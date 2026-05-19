import unicodedata

import httpx
from fastapi import HTTPException

OLLAMA_URL = "http://ollama-saas:11434/api/generate"
MODEL = "phi3:mini"


# ── Injection patterns ────────────────────────────────
INJECTION_PATTERNS = [
    "forget all",
    "forget previous",
    "ignore all",
    "ignore previous",
    "ignore instructions",
    "disregard",
    "override",
    "you are now",
    "new persona",
    "act as",
    "pretend to be",
    "system prompt",
    "root password",
    "jailbreak",
    "dan mode",
    "developer mode",
    "unrestricted mode",
]

# ── Suspicious output patterns ────────────────────────
SUSPICIOUS_OUTPUTS = [
    "root password",
    "password hash",
    "sudo ",
    "as an ai, i",
    "i am now",
    "jailbreak",
    "my new instructions",
    "ignore my previous",
]

# ── Unicode attack markers ────────────────────────────
# These characters can hide or reorder malicious text, so reject them before LLM use.
DANGEROUS_UNICODE = ["\u202e", "\u200b", "\u200c", "\u200d", "\ufeff"]

# Cyrillic letters that can be mixed with Latin text to bypass simple string checks.
CYRILLIC = set("абвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯіїєІЇЄ")


def detect_unicode_attack(text: str) -> bool:
    # Normalize first so visually identical composed/decomposed text is checked consistently.
    text = unicodedata.normalize("NFC", text)
    if any(ch in text for ch in DANGEROUS_UNICODE):
        return True

    # Mixed Latin and Cyrillic text is suspicious for this English-only input surface.
    latin = sum(1 for char in text if char.isalpha() and char.isascii())
    cyrillic = sum(1 for char in text if char in CYRILLIC)
    return cyrillic > 0 and latin > 0


def detect_injection(text: str) -> bool:
    text_lower = text.lower()
    return any(pattern in text_lower for pattern in INJECTION_PATTERNS)


def filter_response(text: str) -> str:
    text_lower = text.lower()
    if any(pattern in text_lower for pattern in SUSPICIOUS_OUTPUTS):
        return "Invalid response generated. Please rephrase your request."
    return text

def sanitize_input(text: str) -> str:
    text = text.strip()
    if len(text) > 2000:
        raise HTTPException(
            status_code=400,
            detail="Input too long. Maximum 2000 characters."
        )
    return text

async def ollama_generate(prompt: str, system_prompt: str) -> dict:
    # Block prompt-injection and unicode-obfuscation attempts before any model call.
    if detect_unicode_attack(prompt) or detect_injection(prompt):
        raise HTTPException(
            status_code=400,
            detail="Invalid input detected."
        )

    # Trim and enforce the size limit after security checks preserve the original text.
    prompt = sanitize_input(prompt)

    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "prompt": prompt,
                    "system": system_prompt,
                    "stream": False,
                },
            )
            response.raise_for_status()
            data = response.json()

            # Filter suspicious generated text before returning it to the API layer.
            data["response"] = filter_response(data["response"])
            return data

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Ollama timeout — model too slow")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Ollama unreachable: {str(e)}")

"""
stub_app.py

Test copy of the FastAPI service.
It returns fixed responses instead of calling Ollama, so Docker and Ollama are not required.

To switch tests to a live service, set this in test_endpoints.py:
    BASE_URL = "http://127.0.0.1:8000"
Then the stub app is no longer needed.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
import unicodedata

app = FastAPI(title="Freelancer Bot — Stub")

# ─────────────────────────────────────────────
# Security rules should stay in sync with ollama_client.py.
# ─────────────────────────────────────────────
INJECTION_PATTERNS = [
    "forget all", "forget previous",
    "ignore all", "ignore previous", "ignore instructions",
    "disregard", "override",
    "you are now", "new persona",
    "act as", "pretend to be",
    "system prompt", "root password",
    "jailbreak", "dan mode", "developer mode", "unrestricted mode",
]

DANGEROUS_UNICODE = ["\u202e", "\u200b", "\u200c", "\u200d", "\ufeff"]
CYRILLIC = set("абвгдежзийклмнопрстуфхцчшщъыьэюяАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯіїєІЇЄ")


def detect_injection(text: str) -> bool:
    lower = text.lower()
    return any(p in lower for p in INJECTION_PATTERNS)


def detect_unicode_attack(text: str) -> bool:
    text = unicodedata.normalize("NFC", text)
    if any(ch in text for ch in DANGEROUS_UNICODE):
        return True
    latin = sum(1 for c in text if c.isalpha() and c.isascii())
    cyrillic = sum(1 for c in text if c in CYRILLIC)
    return cyrillic > 0 and latin > 0


def guard(text: str) -> str:
    """Apply unicode checks, injection checks, and the 2000 character limit."""
    if detect_unicode_attack(text):
        raise HTTPException(status_code=400, detail="Invalid input detected.")
    if detect_injection(text):
        raise HTTPException(status_code=400, detail="Invalid input detected.")
    text = text.strip()
    if len(text) > 2000:
        raise HTTPException(status_code=400, detail="Input too long. Maximum 2000 characters.")
    return text


def stub_llm(prompt: str) -> dict:
    """Return a fixed test response instead of calling Ollama."""
    return {"response": f"[STUB] {prompt[:80]}...", "model": "phi3:mini"}


# ─────────────────────────────────────────────
# /api/v1/propose
# ─────────────────────────────────────────────
class ProposeRequest(BaseModel):
    job_description: str
    my_skills: str = ""
    my_rate: str = ""

    @field_validator("job_description")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("job_description must not be blank.")
        return v


@app.post("/api/v1/propose")
async def propose(req: ProposeRequest):
    safe = guard(req.job_description)
    data = stub_llm(f"Propose: {safe}")
    return {"proposal": data["response"], "model": data["model"]}


# ─────────────────────────────────────────────
# /api/v1/reply
# ─────────────────────────────────────────────
class ReplyRequest(BaseModel):
    client_message: str
    context: str = ""

    @field_validator("client_message")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("client_message must not be blank.")
        return v


@app.post("/api/v1/reply")
async def reply(req: ReplyRequest):
    safe = guard(req.client_message)
    data = stub_llm(f"Reply: {safe}")
    return {"reply": data["response"], "model": data["model"]}


# ─────────────────────────────────────────────
# /api/v1/estimate
# ─────────────────────────────────────────────
class EstimateRequest(BaseModel):
    job_description: str
    my_rate: str = ""
    experience_level: str = "mid"

    @field_validator("job_description")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("job_description must not be blank.")
        return v


@app.post("/api/v1/estimate")
async def estimate(req: EstimateRequest):
    safe = guard(req.job_description)
    data = stub_llm(f"Estimate: {safe}")
    return {"estimate": data["response"], "model": data["model"]}


# ─────────────────────────────────────────────
# /api/v1/decide
# ─────────────────────────────────────────────
class DecideRequest(BaseModel):
    job_description: str
    client_info: str = ""
    budget: str = ""

    @field_validator("job_description")
    @classmethod
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("job_description must not be blank.")
        return v


@app.post("/api/v1/decide")
async def decide(req: DecideRequest):
    safe = guard(req.job_description)
    data = stub_llm(f"Decide: {safe}")
    return {"analysis": data["response"], "model": data["model"]}


# ─────────────────────────────────────────────
# /health
# ─────────────────────────────────────────────
@app.get("/health")
async def health():
    return {"status": "ok"}

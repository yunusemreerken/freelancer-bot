"""
app/routers/base.py

Generic router factory used by all 4 endpoints.
Each endpoint just defines:
  - its route path
  - its system prompt
  - its extra fields (beyond the shared ones)
  - how to build the LLM prompt string
  - its response key name

Nothing else is repeated anywhere.
"""

from typing import Any, Callable, Type
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.ollama_client import ollama_generate


def make_router(
    path: str,
    system_prompt: str,
    request_model: Type[BaseModel],
    response_key: str,
    build_prompt: Callable[[BaseModel], str],
) -> APIRouter:
    """
    Factory that returns a fully-wired APIRouter.

    Args:
        path           : Route path, e.g. "/propose"
        system_prompt  : System prompt sent to Ollama
        request_model  : Pydantic model for the request body
        response_key   : Key name in the JSON response, e.g. "proposal"
        build_prompt   : Function(request) → prompt string for Ollama
    """
    router = APIRouter()

    @router.post(path)
    async def _handler(request: request_model) -> dict[str, Any]:  # type: ignore[valid-type]
        prompt = build_prompt(request)
        data = await ollama_generate(prompt, system_prompt)
        return {response_key: data["response"], "model": data["model"]}

    @router.get(path)
    async def _method_not_allowed() -> None:
        # Declare GET explicitly because the mounted static app would otherwise turn it into 404.
        raise HTTPException(status_code=405, detail="Method not allowed.")

    return router

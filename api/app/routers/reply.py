from pydantic import BaseModel, field_validator
from app.prompts import REPLY_SYSTEM_PROMPT
from app.routers.base import make_router


class ReplyRequest(BaseModel):
    client_message: str
    context: str = ""

    @field_validator("client_message")
    @classmethod
    def not_blank(cls, value: str) -> str:
        # Reject blank input at schema validation time so clients receive a 422 response.
        if not value.strip():
            raise ValueError("client_message must not be blank.")
        return value


def _build_prompt(r: ReplyRequest) -> str:
    return (
        f"Client Message:\n{r.client_message}\n\n"
        f"Project Context: {r.context}\n\n"
        "Write a professional reply to this client message."
    )


router = make_router(
    path="/reply",
    system_prompt=REPLY_SYSTEM_PROMPT,
    request_model=ReplyRequest,
    response_key="reply",
    build_prompt=_build_prompt,
)

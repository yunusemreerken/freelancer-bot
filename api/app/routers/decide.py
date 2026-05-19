from pydantic import BaseModel, field_validator
from app.prompts import DECIDE_SYSTEM_PROMPT
from app.routers.base import make_router


class DecideRequest(BaseModel):
    job_description: str
    client_info: str = ""
    budget: str = ""

    @field_validator("job_description")
    @classmethod
    def not_blank(cls, value: str) -> str:
        # Reject blank input at schema validation time so clients receive a 422 response.
        if not value.strip():
            raise ValueError("job_description must not be blank.")
        return value


def _build_prompt(r: DecideRequest) -> str:
    return (
        f"Job Description:\n{r.job_description}\n\n"
        f"Client Info: {r.client_info}\n"
        f"Budget: {r.budget}\n\n"
        "Analyze this project. List risks, red flags, and key questions to ask."
    )


router = make_router(
    path="/decide",
    system_prompt=DECIDE_SYSTEM_PROMPT,
    request_model=DecideRequest,
    response_key="analysis",
    build_prompt=_build_prompt,
)

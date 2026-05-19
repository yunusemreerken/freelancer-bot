from pydantic import BaseModel, field_validator
from app.prompts import PROPOSE_SYSTEM_PROMPT
from app.routers.base import make_router


class ProposeRequest(BaseModel):
    job_description: str
    my_skills: str = ""
    my_rate: str = ""

    @field_validator("job_description")
    @classmethod
    def not_blank(cls, value: str) -> str:
        # Reject blank input at schema validation time so clients receive a 422 response.
        if not value.strip():
            raise ValueError("job_description must not be blank.")
        return value


def _build_prompt(r: ProposeRequest) -> str:
    return (
        f"Job Description:\n{r.job_description}\n\n"
        f"My Skills: {r.my_skills}\n"
        f"My Rate: {r.my_rate}\n\n"
        "Write a winning freelance proposal for this job."
    )


router = make_router(
    path="/propose",
    system_prompt=PROPOSE_SYSTEM_PROMPT,
    request_model=ProposeRequest,
    response_key="proposal",
    build_prompt=_build_prompt,
)

from pydantic import BaseModel, field_validator
from app.prompts import ESTIMATE_SYSTEM_PROMPT
from app.routers.base import make_router


class EstimateRequest(BaseModel):
    job_description: str
    my_rate: str = ""
    experience_level: str = "mid"

    @field_validator("job_description")
    @classmethod
    def not_blank(cls, value: str) -> str:
        # Reject blank input at schema validation time so clients receive a 422 response.
        if not value.strip():
            raise ValueError("job_description must not be blank.")
        return value


def _build_prompt(r: EstimateRequest) -> str:
    return (
        f"Job Description:\n{r.job_description}\n\n"
        f"My Hourly Rate: {r.my_rate}\n"
        f"Experience Level: {r.experience_level}\n\n"
        "Provide a detailed cost and time estimate for this project."
    )


router = make_router(
    path="/estimate",
    system_prompt=ESTIMATE_SYSTEM_PROMPT,
    request_model=EstimateRequest,
    response_key="estimate",
    build_prompt=_build_prompt,
)

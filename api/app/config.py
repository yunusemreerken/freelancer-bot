"""
Freelancer profile configuration for the API.

This module centralizes profile and rate-card values so future prompt builders
can import one stable object instead of reading environment variables directly.
"""

import os
from dataclasses import dataclass, field


def _split_env_list(value: str) -> list[str]:
    # Parse comma-separated environment values while ignoring empty items.
    return [item.strip() for item in value.split(",") if item.strip()]


def _float_env(name: str, default: float) -> float:
    # Fall back to a safe default when an env value is missing or malformed.
    try:
        return float(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


@dataclass
class FreelancerProfile:
    """Profile and pricing defaults for the local freelancer assistant."""

    name: str = field(default_factory=lambda: os.getenv("FREELANCER_NAME", "Your Name"))
    title: str = field(default_factory=lambda: os.getenv("FREELANCER_TITLE", "Full Stack Developer"))
    skills: list[str] = field(
        default_factory=lambda: _split_env_list(
            os.getenv("FREELANCER_SKILLS", "Python, FastAPI, Docker, AI")
        )
    )
    hourly_rate: float = field(
        default_factory=lambda: _float_env("FREELANCER_HOURLY_RATE", 25.0)
    )
    min_project_budget: float = field(
        default_factory=lambda: _float_env("FREELANCER_MIN_BUDGET", 100.0)
    )
    currency: str = field(default_factory=lambda: os.getenv("FREELANCER_CURRENCY", "USD"))
    timezone: str = field(default_factory=lambda: os.getenv("GENERIC_TIMEZONE", "Europe/Istanbul"))
    languages: list[str] = field(
        default_factory=lambda: _split_env_list(os.getenv("FREELANCER_LANGUAGES", "English"))
    )


# Export one shared profile instance so other modules can import a stable config object.
profile = FreelancerProfile()

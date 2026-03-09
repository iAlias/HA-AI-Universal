import os


class Config:
    """Configuration for the AI Router."""

    provider = os.getenv("AI_PROVIDER", "openai")

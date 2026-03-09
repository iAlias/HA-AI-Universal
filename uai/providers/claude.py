import os

import requests

from .base import BaseProvider


class ClaudeProvider(BaseProvider):
    """Provider adapter for Anthropic Claude."""

    def generate(self, prompt):
        url = "https://api.anthropic.com/v1/messages"

        headers = {
            "x-api-key": os.getenv("ANTHROPIC_API_KEY"),
        }

        data = {
            "model": "claude-3-opus-20240229",
            "max_tokens": 4096,
            "messages": [
                {"role": "user", "content": prompt},
            ],
        }

        r = requests.post(url, json=data, headers=headers, timeout=60)
        r.raise_for_status()

        return r.json()["content"][0]["text"]

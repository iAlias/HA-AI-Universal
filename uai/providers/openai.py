import os

import requests

from .base import BaseProvider


class OpenAIProvider(BaseProvider):
    """Provider adapter for OpenAI (ChatGPT)."""

    def generate(self, prompt):
        url = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        }

        data = {
            "model": "gpt-4o",
            "messages": [
                {"role": "user", "content": prompt},
            ],
        }

        r = requests.post(url, json=data, headers=headers, timeout=60)
        r.raise_for_status()

        return r.json()["choices"][0]["message"]["content"]

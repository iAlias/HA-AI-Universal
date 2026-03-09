import os

import requests

from .base import BaseProvider


class CopilotProvider(BaseProvider):
    """Provider adapter for GitHub Copilot."""

    def generate(self, prompt):
        url = "https://api.githubcopilot.com/chat/completions"

        headers = {
            "Authorization": f"Bearer {os.getenv('COPILOT_API_KEY')}",
        }

        data = {
            "model": "copilot-chat",
            "messages": [
                {"role": "user", "content": prompt},
            ],
        }

        r = requests.post(url, json=data, headers=headers, timeout=60)
        r.raise_for_status()

        return r.json()["choices"][0]["message"]["content"]

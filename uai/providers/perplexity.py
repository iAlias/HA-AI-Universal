import os

import requests

from .base import BaseProvider


class PerplexityProvider(BaseProvider):
    """Provider adapter for Perplexity AI."""

    def generate(self, prompt):
        url = "https://api.perplexity.ai/chat/completions"

        headers = {
            "Authorization": f"Bearer {os.getenv('PERPLEXITY_API_KEY')}",
        }

        data = {
            "model": "sonar-small-chat",
            "messages": [
                {"role": "user", "content": prompt},
            ],
        }

        r = requests.post(url, json=data, headers=headers, timeout=60)
        r.raise_for_status()

        return r.json()["choices"][0]["message"]["content"]

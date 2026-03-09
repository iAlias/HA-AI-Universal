import os

import requests

from .base import BaseProvider


class GeminiProvider(BaseProvider):
    """Provider adapter for Google Gemini."""

    def generate(self, prompt):
        api_key = os.getenv("GEMINI_API_KEY")
        url = (
            "https://generativelanguage.googleapis.com/v1beta/"
            f"models/gemini-pro:generateContent?key={api_key}"
        )

        data = {
            "contents": [
                {
                    "parts": [{"text": prompt}],
                },
            ],
        }

        r = requests.post(url, json=data, timeout=60)
        r.raise_for_status()

        return r.json()["candidates"][0]["content"]["parts"][0]["text"]

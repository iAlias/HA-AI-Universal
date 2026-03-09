"""Multi-LLM bridge for AI Universal integration."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from .const import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    DEFAULT_MODELS,
    HOME_ASSISTANT_EXPERT_PROMPT,
    PROVIDER_ANTHROPIC,
    PROVIDER_GEMINI,
    PROVIDER_OPENAI,
    PROVIDER_PERPLEXITY,
)

_LOGGER = logging.getLogger(__name__)


class AIUniversalBridge:
    """Bridge that routes requests to various LLM providers."""

    def __init__(
        self,
        provider: str,
        api_key: str,
        model: str | None = None,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = DEFAULT_TEMPERATURE,
        system_prompt: str = HOME_ASSISTANT_EXPERT_PROMPT,
    ) -> None:
        """Initialize the bridge."""
        self.provider = provider
        self.api_key = api_key
        self.model = model or DEFAULT_MODELS.get(provider, "")
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.system_prompt = system_prompt

    async def async_validate(self) -> None:
        """Validate that the API key and provider configuration are valid."""
        await self.async_generate("Hello")

    async def async_generate(
        self,
        prompt: str,
        conversation_history: list[dict[str, str]] | None = None,
    ) -> str:
        """Generate a response from the configured LLM provider."""
        if self.provider == PROVIDER_OPENAI:
            return await self._openai_generate(prompt, conversation_history)
        if self.provider == PROVIDER_ANTHROPIC:
            return await self._anthropic_generate(prompt, conversation_history)
        if self.provider == PROVIDER_GEMINI:
            return await self._gemini_generate(prompt, conversation_history)
        if self.provider == PROVIDER_PERPLEXITY:
            return await self._perplexity_generate(prompt, conversation_history)
        raise ValueError(f"Unsupported provider: {self.provider}")

    async def _openai_generate(
        self,
        prompt: str,
        history: list[dict[str, str]] | None,
    ) -> str:
        """Generate a response using the OpenAI API."""
        try:
            from openai import AsyncOpenAI  # noqa: PLC0415
        except ImportError as err:
            raise ImportError("openai package is required for OpenAI provider") from err

        client = AsyncOpenAI(api_key=self.api_key)
        messages = self._build_openai_messages(prompt, history)

        response = await client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        return response.choices[0].message.content or ""

    async def _anthropic_generate(
        self,
        prompt: str,
        history: list[dict[str, str]] | None,
    ) -> str:
        """Generate a response using the Anthropic Claude API."""
        try:
            import anthropic  # noqa: PLC0415
        except ImportError as err:
            raise ImportError(
                "anthropic package is required for Anthropic provider"
            ) from err

        client = anthropic.AsyncAnthropic(api_key=self.api_key)
        messages = self._build_anthropic_messages(prompt, history)

        response = await client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=self.system_prompt,
            messages=messages,
        )
        return response.content[0].text if response.content else ""

    async def _gemini_generate(
        self,
        prompt: str,
        history: list[dict[str, str]] | None,
    ) -> str:
        """Generate a response using the Google Gemini API."""
        try:
            import google.generativeai as genai  # noqa: PLC0415
        except ImportError as err:
            raise ImportError(
                "google-generativeai package is required for Gemini provider"
            ) from err

        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(
            model_name=self.model,
            system_instruction=self.system_prompt,
            generation_config=genai.GenerationConfig(
                max_output_tokens=self.max_tokens,
                temperature=self.temperature,
            ),
        )

        gemini_history = self._build_gemini_history(history)
        chat = model.start_chat(history=gemini_history)

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, chat.send_message, prompt)
        return response.text

    async def _perplexity_generate(
        self,
        prompt: str,
        history: list[dict[str, str]] | None,
    ) -> str:
        """Generate a response using the Perplexity API (OpenAI-compatible)."""
        try:
            from openai import AsyncOpenAI  # noqa: PLC0415
        except ImportError as err:
            raise ImportError("openai package is required for Perplexity provider") from err

        client = AsyncOpenAI(
            api_key=self.api_key,
            base_url="https://api.perplexity.ai",
        )
        messages = self._build_openai_messages(prompt, history)

        response = await client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        return response.choices[0].message.content or ""

    def _build_openai_messages(
        self,
        prompt: str,
        history: list[dict[str, str]] | None,
    ) -> list[dict[str, str]]:
        """Build message list for OpenAI-compatible APIs."""
        messages: list[dict[str, str]] = [
            {"role": "system", "content": self.system_prompt}
        ]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": prompt})
        return messages

    def _build_anthropic_messages(
        self,
        prompt: str,
        history: list[dict[str, str]] | None,
    ) -> list[dict[str, str]]:
        """Build message list for Anthropic API (no system message in list)."""
        messages: list[dict[str, str]] = []
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": prompt})
        return messages

    def _build_gemini_history(
        self,
        history: list[dict[str, str]] | None,
    ) -> list[dict[str, Any]]:
        """Convert OpenAI-style history to Gemini format."""
        if not history:
            return []
        gemini_history = []
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg["content"]]})
        return gemini_history

"""Tests for the AI Universal Multi-LLM Bridge."""

from __future__ import annotations

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

import sys
import os

# Allow importing from the custom_components directory without a full HA install
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from custom_components.ai_universal.const import (
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODELS,
    DEFAULT_TEMPERATURE,
    HOME_ASSISTANT_EXPERT_PROMPT,
    PROVIDER_ANTHROPIC,
    PROVIDER_GEMINI,
    PROVIDER_OPENAI,
    PROVIDER_PERPLEXITY,
)
from custom_components.ai_universal.llm_bridge import AIUniversalBridge


# ---------------------------------------------------------------------------
# AIUniversalBridge construction
# ---------------------------------------------------------------------------


def test_bridge_defaults():
    """Test that bridge uses correct defaults from const."""
    bridge = AIUniversalBridge(provider=PROVIDER_OPENAI, api_key="sk-test")
    assert bridge.provider == PROVIDER_OPENAI
    assert bridge.api_key == "sk-test"
    assert bridge.model == DEFAULT_MODELS[PROVIDER_OPENAI]
    assert bridge.max_tokens == DEFAULT_MAX_TOKENS
    assert bridge.temperature == DEFAULT_TEMPERATURE
    assert bridge.system_prompt == HOME_ASSISTANT_EXPERT_PROMPT


def test_bridge_custom_values():
    """Test that custom values override defaults."""
    bridge = AIUniversalBridge(
        provider=PROVIDER_ANTHROPIC,
        api_key="sk-ant-test",
        model="claude-3-opus-20240229",
        max_tokens=512,
        temperature=0.2,
        system_prompt="Custom prompt",
    )
    assert bridge.model == "claude-3-opus-20240229"
    assert bridge.max_tokens == 512
    assert bridge.temperature == 0.2
    assert bridge.system_prompt == "Custom prompt"


@pytest.mark.asyncio
async def test_bridge_invalid_provider_raises():
    """Test that an unsupported provider raises ValueError on generate."""
    bridge = AIUniversalBridge(provider="unsupported", api_key="key")

    with pytest.raises(ValueError, match="Unsupported provider"):
        await bridge.async_generate("Hello")


# ---------------------------------------------------------------------------
# Message-building helpers
# ---------------------------------------------------------------------------


def test_build_openai_messages_no_history():
    """System prompt + user message when no history."""
    bridge = AIUniversalBridge(provider=PROVIDER_OPENAI, api_key="k")
    msgs = bridge._build_openai_messages("Hi", None)
    assert msgs[0] == {"role": "system", "content": bridge.system_prompt}
    assert msgs[-1] == {"role": "user", "content": "Hi"}
    assert len(msgs) == 2


def test_build_openai_messages_with_history():
    """History is inserted between system and latest user message."""
    bridge = AIUniversalBridge(provider=PROVIDER_OPENAI, api_key="k")
    history = [
        {"role": "user", "content": "First"},
        {"role": "assistant", "content": "First reply"},
    ]
    msgs = bridge._build_openai_messages("Second", history)
    assert len(msgs) == 4
    assert msgs[1]["content"] == "First"
    assert msgs[-1] == {"role": "user", "content": "Second"}


def test_build_anthropic_messages_excludes_system():
    """Anthropic messages must NOT contain a system message in the list."""
    bridge = AIUniversalBridge(provider=PROVIDER_ANTHROPIC, api_key="k")
    msgs = bridge._build_anthropic_messages("Hello", None)
    assert all(m["role"] != "system" for m in msgs)
    assert msgs[-1] == {"role": "user", "content": "Hello"}


def test_build_gemini_history_role_mapping():
    """assistant → model for Gemini history."""
    bridge = AIUniversalBridge(provider=PROVIDER_GEMINI, api_key="k")
    history = [
        {"role": "user", "content": "Q"},
        {"role": "assistant", "content": "A"},
    ]
    gemini = bridge._build_gemini_history(history)
    assert gemini[0]["role"] == "user"
    assert gemini[1]["role"] == "model"
    assert gemini[1]["parts"] == ["A"]


def test_build_gemini_history_empty():
    """Empty history returns empty list."""
    bridge = AIUniversalBridge(provider=PROVIDER_GEMINI, api_key="k")
    assert bridge._build_gemini_history(None) == []
    assert bridge._build_gemini_history([]) == []


# ---------------------------------------------------------------------------
# OpenAI provider
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_openai_generate():
    """Mock OpenAI call and verify response text is returned."""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "HA answer"

    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

    mock_openai_module = MagicMock()
    mock_openai_module.AsyncOpenAI.return_value = mock_client

    bridge = AIUniversalBridge(provider=PROVIDER_OPENAI, api_key="sk-test")

    with patch.dict("sys.modules", {"openai": mock_openai_module}):
        result = await bridge._openai_generate("What is HA?", None)

    assert result == "HA answer"


# ---------------------------------------------------------------------------
# Perplexity provider (OpenAI-compatible)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_perplexity_generate():
    """Perplexity uses the OpenAI client pointed at api.perplexity.ai."""
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Perplexity answer"

    mock_client = AsyncMock()
    mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

    mock_openai_module = MagicMock()
    mock_openai_module.AsyncOpenAI.return_value = mock_client

    bridge = AIUniversalBridge(provider=PROVIDER_PERPLEXITY, api_key="pplx-key")

    with patch.dict("sys.modules", {"openai": mock_openai_module}):
        result = await bridge._perplexity_generate("Search query", None)

    assert result == "Perplexity answer"


# ---------------------------------------------------------------------------
# Anthropic provider
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_anthropic_generate():
    """Mock Anthropic call and verify response text is returned."""
    mock_content = MagicMock()
    mock_content.text = "Claude answer"
    mock_response = MagicMock()
    mock_response.content = [mock_content]

    mock_messages = AsyncMock()
    mock_messages.create = AsyncMock(return_value=mock_response)
    mock_client = MagicMock()
    mock_client.messages = mock_messages

    bridge = AIUniversalBridge(provider=PROVIDER_ANTHROPIC, api_key="ant-key")

    mock_anthropic_module = MagicMock()
    mock_anthropic_module.AsyncAnthropic.return_value = mock_client

    with patch.dict("sys.modules", {"anthropic": mock_anthropic_module}):
        result = await bridge._anthropic_generate("Automate lights", None)

    assert result == "Claude answer"


# ---------------------------------------------------------------------------
# HOME_ASSISTANT_EXPERT_PROMPT content
# ---------------------------------------------------------------------------


def test_expert_prompt_covers_key_topics():
    """The expert prompt must mention core Home Assistant topics."""
    prompt = HOME_ASSISTANT_EXPERT_PROMPT
    for keyword in ("automation", "YAML", "Lovelace", "template", "Zigbee"):
        assert keyword.lower() in prompt.lower(), f"Missing keyword: {keyword}"

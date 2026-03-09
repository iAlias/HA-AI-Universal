"""Conversation agent for AI Universal Multi-LLM Bridge."""

from __future__ import annotations

import logging
from typing import Any, Literal

from homeassistant.components import conversation
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import intent
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .llm_bridge import AIUniversalBridge

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the AI Universal conversation agent from a config entry."""
    bridge: AIUniversalBridge = hass.data[DOMAIN][config_entry.entry_id]
    agent = AIUniversalConversationEntity(config_entry, bridge)
    async_add_entities([agent])


class AIUniversalConversationEntity(
    conversation.ConversationEntity, conversation.AbstractConversationAgent
):
    """AI Universal conversation agent that routes to multiple LLM providers."""

    _attr_has_entity_name = True
    _attr_name = None

    def __init__(self, entry: ConfigEntry, bridge: AIUniversalBridge) -> None:
        """Initialize the conversation entity."""
        self._entry = entry
        self._bridge = bridge
        self._attr_unique_id = entry.entry_id
        self._attr_device_info = {
            "identifiers": {(DOMAIN, entry.entry_id)},
            "name": entry.title,
            "manufacturer": "AI Universal",
            "model": bridge.provider,
            "sw_version": bridge.model,
        }
        # Maintain per-conversation history keyed by conversation_id
        self._histories: dict[str, list[dict[str, str]]] = {}

    @property
    def supported_languages(self) -> list[str] | Literal["*"]:
        """Return supported languages."""
        return "*"

    async def async_process(
        self, user_input: conversation.ConversationInput
    ) -> conversation.ConversationResult:
        """Process a sentence from the user and return an AI-generated response."""
        conversation_id = user_input.conversation_id or user_input.device_id or "default"

        history = self._histories.get(conversation_id, [])

        try:
            response_text = await self._bridge.async_generate(
                prompt=user_input.text,
                conversation_history=history,
            )
        except Exception as err:
            _LOGGER.error("Error generating response from %s: %s", self._bridge.provider, err)
            response_text = (
                f"I'm sorry, I encountered an error communicating with "
                f"{self._bridge.provider}. Please check your API key and network "
                f"connection."
            )

        # Update history for multi-turn conversations
        history = history + [
            {"role": "user", "content": user_input.text},
            {"role": "assistant", "content": response_text},
        ]
        # Keep the last 20 turns (40 messages) to avoid token overflow
        self._histories[conversation_id] = history[-40:]

        response = intent.IntentResponse(language=user_input.language)
        response.async_set_speech(response_text)
        return conversation.ConversationResult(
            response=response,
            conversation_id=conversation_id,
        )

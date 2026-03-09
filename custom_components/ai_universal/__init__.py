"""AI Universal Multi-LLM Bridge integration."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.helpers.typing import ConfigType

from .const import (
    CONF_API_KEY,
    CONF_MAX_TOKENS,
    CONF_MODEL,
    CONF_PROVIDER,
    CONF_SYSTEM_PROMPT,
    CONF_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    DOMAIN,
    HOME_ASSISTANT_EXPERT_PROMPT,
)
from .llm_bridge import AIUniversalBridge

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[str] = ["conversation"]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up AI Universal component."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AI Universal from a config entry."""
    provider = entry.data[CONF_PROVIDER]
    api_key = entry.data[CONF_API_KEY]
    model = entry.data.get(CONF_MODEL)
    max_tokens = entry.options.get(CONF_MAX_TOKENS, DEFAULT_MAX_TOKENS)
    temperature = entry.options.get(CONF_TEMPERATURE, DEFAULT_TEMPERATURE)
    system_prompt = entry.options.get(CONF_SYSTEM_PROMPT, HOME_ASSISTANT_EXPERT_PROMPT)

    bridge = AIUniversalBridge(
        provider=provider,
        api_key=api_key,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system_prompt=system_prompt,
    )

    try:
        await bridge.async_validate()
    except Exception as err:
        raise ConfigEntryNotReady(f"Unable to connect to {provider}: {err}") from err

    hass.data[DOMAIN][entry.entry_id] = bridge

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(async_update_options))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update options for an existing config entry."""
    await hass.config_entries.async_reload(entry.entry_id)

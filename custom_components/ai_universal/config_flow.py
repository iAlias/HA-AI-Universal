"""Config flow for AI Universal Multi-LLM Bridge integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, OptionsFlow
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import (
    NumberSelector,
    NumberSelectorConfig,
    NumberSelectorMode,
    SelectSelector,
    SelectSelectorConfig,
    SelectSelectorMode,
    TextSelector,
    TextSelectorConfig,
    TextSelectorType,
)

from .const import (
    AVAILABLE_MODELS,
    CONF_API_KEY,
    CONF_MAX_TOKENS,
    CONF_MODEL,
    CONF_PROVIDER,
    CONF_SYSTEM_PROMPT,
    CONF_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
    DEFAULT_MODELS,
    DEFAULT_TEMPERATURE,
    DOMAIN,
    HOME_ASSISTANT_EXPERT_PROMPT,
    PROVIDERS,
)

_LOGGER = logging.getLogger(__name__)


class AIUniversalConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AI Universal."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._provider: str | None = None

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step: choose provider."""
        errors: dict[str, str] = {}

        if user_input is not None:
            self._provider = user_input[CONF_PROVIDER]
            return await self.async_step_api_key()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_NAME, default="AI Universal"): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.TEXT)
                    ),
                    vol.Required(CONF_PROVIDER): SelectSelector(
                        SelectSelectorConfig(
                            options=PROVIDERS,
                            mode=SelectSelectorMode.LIST,
                            translation_key="provider",
                        )
                    ),
                }
            ),
            errors=errors,
        )

    async def async_step_api_key(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle API key and model entry."""
        errors: dict[str, str] = {}
        provider = self._provider or ""
        default_model = DEFAULT_MODELS.get(provider, "")
        available_models = AVAILABLE_MODELS.get(provider, [default_model])

        if user_input is not None:
            from .llm_bridge import AIUniversalBridge  # noqa: PLC0415

            bridge = AIUniversalBridge(
                provider=provider,
                api_key=user_input[CONF_API_KEY],
                model=user_input.get(CONF_MODEL, default_model),
            )
            try:
                await bridge.async_validate()
            except Exception:
                _LOGGER.exception("Error validating API key for %s", provider)
                errors["base"] = "cannot_connect"
            else:
                return self.async_create_entry(
                    title=f"AI Universal ({provider})",
                    data={
                        CONF_PROVIDER: provider,
                        CONF_API_KEY: user_input[CONF_API_KEY],
                        CONF_MODEL: user_input.get(CONF_MODEL, default_model),
                    },
                )

        return self.async_show_form(
            step_id="api_key",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): TextSelector(
                        TextSelectorConfig(type=TextSelectorType.PASSWORD)
                    ),
                    vol.Required(CONF_MODEL, default=default_model): SelectSelector(
                        SelectSelectorConfig(
                            options=available_models,
                            mode=SelectSelectorMode.LIST,
                        )
                    ),
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> AIUniversalOptionsFlow:
        """Return the options flow handler."""
        return AIUniversalOptionsFlow(config_entry)


class AIUniversalOptionsFlow(OptionsFlow):
    """Handle options for the AI Universal integration."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Manage the AI Universal options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        options = self.config_entry.options
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        CONF_SYSTEM_PROMPT,
                        default=options.get(
                            CONF_SYSTEM_PROMPT, HOME_ASSISTANT_EXPERT_PROMPT
                        ),
                    ): TextSelector(
                        TextSelectorConfig(
                            type=TextSelectorType.TEXT,
                            multiline=True,
                        )
                    ),
                    vol.Optional(
                        CONF_MAX_TOKENS,
                        default=options.get(CONF_MAX_TOKENS, DEFAULT_MAX_TOKENS),
                    ): NumberSelector(
                        NumberSelectorConfig(
                            min=64,
                            max=8192,
                            step=64,
                            mode=NumberSelectorMode.BOX,
                        )
                    ),
                    vol.Optional(
                        CONF_TEMPERATURE,
                        default=options.get(CONF_TEMPERATURE, DEFAULT_TEMPERATURE),
                    ): NumberSelector(
                        NumberSelectorConfig(
                            min=0.0,
                            max=2.0,
                            step=0.05,
                            mode=NumberSelectorMode.SLIDER,
                        )
                    ),
                }
            ),
        )

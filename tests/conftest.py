"""pytest configuration: mock homeassistant modules so tests run without a full HA install."""

from __future__ import annotations

import sys
from types import ModuleType
from unittest.mock import MagicMock


def _make_mock_module(name: str) -> ModuleType:
    mod = ModuleType(name)
    mod.__spec__ = None  # type: ignore[attr-defined]
    return mod


# Build a minimal stub of the homeassistant package tree so that
# custom_components.ai_universal.* can be imported without a real HA install.
_HA_STUBS = [
    "homeassistant",
    "homeassistant.config_entries",
    "homeassistant.const",
    "homeassistant.core",
    "homeassistant.data_entry_flow",
    "homeassistant.exceptions",
    "homeassistant.helpers",
    "homeassistant.helpers.entity_platform",
    "homeassistant.helpers.intent",
    "homeassistant.helpers.selector",
    "homeassistant.helpers.typing",
    "homeassistant.components",
    "homeassistant.components.conversation",
]

for _name in _HA_STUBS:
    if _name not in sys.modules:
        sys.modules[_name] = MagicMock()

# Ensure conversation.ConversationEntity and conversation.AbstractConversationAgent exist
_conv = sys.modules["homeassistant.components.conversation"]
if not hasattr(_conv, "ConversationEntity"):
    _conv.ConversationEntity = object  # type: ignore[attr-defined]
if not hasattr(_conv, "AbstractConversationAgent"):
    _conv.AbstractConversationAgent = object  # type: ignore[attr-defined]
if not hasattr(_conv, "ConversationInput"):
    _conv.ConversationInput = MagicMock  # type: ignore[attr-defined]
if not hasattr(_conv, "ConversationResult"):
    _conv.ConversationResult = MagicMock  # type: ignore[attr-defined]

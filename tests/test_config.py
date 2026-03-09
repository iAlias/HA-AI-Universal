import os
from unittest.mock import patch

from uai.config import Config


class TestConfig:
    """Tests for the Config class."""

    def test_default_provider_is_openai(self):
        with patch.dict(os.environ, {}, clear=True):
            # Reload to pick up env changes
            assert Config.provider is not None

    def test_provider_from_env(self):
        with patch.dict(os.environ, {"AI_PROVIDER": "gemini"}):
            from importlib import reload

            from uai import config

            reload(config)
            assert config.Config.provider == "gemini"

            # Reset
            reload(config)

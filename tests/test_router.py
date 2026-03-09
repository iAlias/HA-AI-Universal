from unittest.mock import MagicMock, patch

from uai.providers.base import BaseProvider
from uai.router import AIRouter


class TestAIRouter:
    """Tests for the AIRouter class."""

    def test_ask_delegates_to_active_provider(self):
        router = AIRouter()
        mock_provider = MagicMock(spec=BaseProvider)
        mock_provider.generate.return_value = "test response"
        router.providers["openai"] = mock_provider
        router.active = "openai"

        result = router.ask("hello")

        assert result == "test response"
        mock_provider.generate.assert_called_once_with("hello")

    def test_use_switches_provider(self):
        router = AIRouter()
        router.use("gemini")

        assert router.active == "gemini"

    def test_use_raises_on_unknown_provider(self):
        router = AIRouter()

        try:
            router.use("unknown")
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "Unknown provider" in str(e)

    def test_fallback_on_failure(self):
        router = AIRouter()

        # Make the active provider fail
        mock_active = MagicMock(spec=BaseProvider)
        mock_active.generate.side_effect = Exception("API error")

        # Make a fallback provider succeed
        mock_fallback = MagicMock(spec=BaseProvider)
        mock_fallback.generate.return_value = "fallback response"

        router.providers["openai"] = mock_active
        router.providers["gemini"] = mock_fallback
        router.active = "openai"

        result = router.ask("hello")

        assert result == "fallback response"

    def test_all_providers_fail_raises(self):
        router = AIRouter()

        # Make all providers fail
        for name in router.providers:
            mock_provider = MagicMock(spec=BaseProvider)
            mock_provider.generate.side_effect = Exception("API error")
            router.providers[name] = mock_provider

        try:
            router.ask("hello")
            assert False, "Should have raised RuntimeError"
        except RuntimeError as e:
            assert "All providers failed" in str(e)

    def test_stream_delegates_to_active_provider(self):
        router = AIRouter()
        mock_provider = MagicMock(spec=BaseProvider)
        mock_provider.stream.return_value = iter(["a", "b", "c"])
        router.providers["openai"] = mock_provider
        router.active = "openai"

        result = list(router.stream("hello"))

        assert result == ["a", "b", "c"]

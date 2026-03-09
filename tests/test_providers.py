from uai.providers.base import BaseProvider


class TestBaseProvider:
    """Tests for the BaseProvider class."""

    def test_generate_raises_not_implemented(self):
        provider = BaseProvider()

        try:
            provider.generate("hello")
            assert False, "Should have raised NotImplementedError"
        except NotImplementedError:
            pass

    def test_stream_raises_not_implemented(self):
        provider = BaseProvider()

        try:
            provider.stream("hello")
            assert False, "Should have raised NotImplementedError"
        except NotImplementedError:
            pass

    def test_healthcheck_returns_true(self):
        provider = BaseProvider()

        assert provider.healthcheck() is True

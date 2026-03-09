class BaseProvider:
    """Base class for all AI providers."""

    def generate(self, prompt):
        """Generate a response from the AI provider."""
        raise NotImplementedError()

    def stream(self, prompt):
        """Stream a response from the AI provider."""
        raise NotImplementedError()

    def healthcheck(self):
        """Check if the provider is available."""
        return True

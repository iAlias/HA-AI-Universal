from .config import Config
from .providers.claude import ClaudeProvider
from .providers.copilot import CopilotProvider
from .providers.gemini import GeminiProvider
from .providers.openai import OpenAIProvider
from .providers.perplexity import PerplexityProvider


class AIRouter:
    """Universal AI Router with automatic fallback."""

    def __init__(self):
        self.providers = {
            "openai": OpenAIProvider(),
            "gemini": GeminiProvider(),
            "claude": ClaudeProvider(),
            "perplexity": PerplexityProvider(),
            "copilot": CopilotProvider(),
        }
        self.active = Config.provider

    def use(self, provider_name):
        """Switch to a different AI provider."""
        if provider_name not in self.providers:
            raise ValueError(
                f"Unknown provider: {provider_name}. "
                f"Available: {list(self.providers.keys())}"
            )
        self.active = provider_name

    def ask(self, prompt):
        """Generate a response using the active provider with fallback."""
        provider = self.providers[self.active]

        try:
            return provider.generate(prompt)
        except Exception:
            return self._fallback(prompt)

    def stream(self, prompt):
        """Stream a response from the active provider."""
        provider = self.providers[self.active]
        return provider.stream(prompt)

    def _fallback(self, prompt):
        """Try other providers if the active one fails."""
        for name, provider in self.providers.items():
            if name == self.active:
                continue

            try:
                return provider.generate(prompt)
            except Exception:
                continue

        raise RuntimeError("All providers failed")

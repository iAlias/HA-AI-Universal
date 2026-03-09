"""Constants for the AI Universal Multi-LLM Bridge integration."""

DOMAIN = "ai_universal"
CONF_PROVIDER = "provider"
CONF_API_KEY = "api_key"
CONF_MODEL = "model"
CONF_MAX_TOKENS = "max_tokens"
CONF_TEMPERATURE = "temperature"
CONF_SYSTEM_PROMPT = "system_prompt"

PROVIDER_OPENAI = "openai"
PROVIDER_ANTHROPIC = "anthropic"
PROVIDER_GEMINI = "gemini"
PROVIDER_PERPLEXITY = "perplexity"

PROVIDERS = [
    PROVIDER_OPENAI,
    PROVIDER_ANTHROPIC,
    PROVIDER_GEMINI,
    PROVIDER_PERPLEXITY,
]

DEFAULT_MODELS = {
    PROVIDER_OPENAI: "gpt-4o",
    PROVIDER_ANTHROPIC: "claude-3-5-sonnet-20241022",
    PROVIDER_GEMINI: "gemini-1.5-pro",
    PROVIDER_PERPLEXITY: "llama-3.1-sonar-large-128k-online",
}

AVAILABLE_MODELS = {
    PROVIDER_OPENAI: [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4-turbo",
        "gpt-3.5-turbo",
    ],
    PROVIDER_ANTHROPIC: [
        "claude-3-5-sonnet-20241022",
        "claude-3-5-haiku-20241022",
        "claude-3-opus-20240229",
    ],
    PROVIDER_GEMINI: [
        "gemini-1.5-pro",
        "gemini-1.5-flash",
        "gemini-2.0-flash-exp",
    ],
    PROVIDER_PERPLEXITY: [
        "llama-3.1-sonar-large-128k-online",
        "llama-3.1-sonar-small-128k-online",
        "llama-3.1-sonar-huge-128k-online",
    ],
}

DEFAULT_MAX_TOKENS = 2048
DEFAULT_TEMPERATURE = 0.7

HOME_ASSISTANT_EXPERT_PROMPT = (
    "You are a Home Assistant expert and AI assistant integrated directly into "
    "a Home Assistant instance. You have deep knowledge of:\n"
    "- Home Assistant configuration (YAML, config entries, automations, scripts, scenes)\n"
    "- Home Assistant integrations and custom components\n"
    "- Smart home devices, protocols (Zigbee, Z-Wave, Matter, Thread, Wi-Fi, Bluetooth)\n"
    "- Home Assistant templating (Jinja2), helpers, and the entity registry\n"
    "- Home Assistant dashboards (Lovelace), custom cards, and themes\n"
    "- Energy management, statistics, and long-term storage\n"
    "- Home Assistant automations, Node-RED, and AppDaemon\n"
    "- Security best practices for smart home systems\n\n"
    "You can help users:\n"
    "- Diagnose and troubleshoot issues\n"
    "- Write and review automations, scripts, and templates\n"
    "- Recommend integrations and configurations\n"
    "- Explain Home Assistant concepts clearly\n\n"
    "Always provide accurate, safe, and actionable advice. "
    "When writing YAML or code examples, ensure they are valid and well-commented."
)

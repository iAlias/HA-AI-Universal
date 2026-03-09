# HA AI Universal

> One API to rule all AIs — Multi-LLM Bridge for Home Assistant

[![HACS Validation](https://github.com/iAlias/HA-AI-Universal/actions/workflows/hacs.yaml/badge.svg)](https://github.com/iAlias/HA-AI-Universal/actions/workflows/hacs.yaml)
[![Hassfest Validation](https://github.com/iAlias/HA-AI-Universal/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/iAlias/HA-AI-Universal/actions/workflows/hassfest.yaml)

HA AI Universal is a Home Assistant custom integration that provides a **universal wrapper** for multiple AI providers. Use a single API to interact with any supported LLM, with automatic fallback if a provider fails.

## Installation

You can install this integration manually or via HACS.

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=iAlias&repository=HA-AI-Universal&category=integration)

### Manual Installation

1. Download the `custom_components/ha_ai_universal` folder from this repository.
2. Copy it into your Home Assistant `config/custom_components/` directory.
3. Restart Home Assistant.

## Configuration

To configure the integration in Home Assistant, set the API key for your preferred provider as an environment variable before starting Home Assistant:

| Variable             | Provider                             | API Key Link                                                      |
| -------------------- | ------------------------------------ | ----------------------------------------------------------------- |
| `OPENAI_API_KEY`     | ChatGPT                              | [OpenAI API keys](https://platform.openai.com/api-keys)          |
| `GEMINI_API_KEY`     | Gemini                               | [Google AI Studio](https://aistudio.google.com/app/apikey)        |
| `ANTHROPIC_API_KEY`  | Claude                               | [Anthropic Console](https://console.anthropic.com/settings/keys)  |
| `PERPLEXITY_API_KEY` | Perplexity AI                        | [Perplexity API keys](https://www.perplexity.ai/account/api/keys) |
| `COPILOT_API_KEY`    | GitHub Copilot                       | [GitHub Settings](https://github.com/settings/tokens)             |
| `AI_PROVIDER`        | Default provider (default: `openai`) | N/A                                                               |

To configure HA AI Universal as a conversation agent for your Voice assistant:

1. Go to **Settings** > **Voice assistants** or use the My Home Assistant link.

[![Open your Home Assistant instance and show your voice assistants.](https://my.home-assistant.io/badges/voice_assistants.svg)](https://my.home-assistant.io/redirect/voice_assistants/)

2. Select **Add assistant**.
3. Enter the assistant's name and select one of the HA AI Universal models as the **Conversation agent**.
4. Now you can customize your conversation agent settings.

## Features

HA AI Universal integration supports:

- Multiple AI providers with a unified interface
- Automatic fallback if a provider fails (`ChatGPT → Gemini → Claude → Perplexity → Copilot`)
- Conversation platform
- AI Task platform
- Runtime provider switching
- Streaming responses

### Supported Providers

| Provider       | Status |
| -------------- | ------ |
| ChatGPT        | ✅      |
| Gemini         | ✅      |
| Claude         | ✅      |
| Perplexity AI  | ✅      |
| GitHub Copilot | ✅      |

## AI Task examples

### Generating a short description of weather conditions

```yaml
action: ai_task.generate_data
data:
  task_name: Weather Description
  entity_id: ai_task.ha_ai_universal
  instructions: >-
    Based on this {{ states.weather.home }} create a short weather
    description (ONLY ONE SENTENCE).
```

### Asking for a code review

```yaml
action: ai_task.generate_data
data:
  task_name: Code Review
  entity_id: ai_task.ha_ai_universal
  instructions: >-
    Review the following code and suggest improvements.
```

## Python Library Usage

This repository also provides a standalone Python library:

```bash
pip install universal-ai
```

```python
from uai import ai

response = ai.ask("Write a REST API in Python")
print(response)
```

### Switch Provider

```python
ai.use("gemini")
ai.ask("Hello!")
```

### API

```python
ai.ask(prompt)          # generate response
ai.stream(prompt)       # stream response
ai.use("provider")      # switch provider
```

## Architecture

```
User
 ↓
AI Router
 ↓
Provider Adapter
 ↓
Provider API
```

See [docs/architecture.md](docs/architecture.md) for details.

## How to debug

To debug the integration add this to your logger configuration:

```yaml
# configuration.yaml file
logger:
  default: warning
  logs:
    custom_components.ha_ai_universal: debug
    uai: debug
```

## How to create a dev environment

```bash
git clone https://github.com/iAlias/HA-AI-Universal.git
cd HA-AI-Universal
pip install -e ".[dev]"
```

## License

MIT

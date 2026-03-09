# HA AI Universal

> One API to rule all AIs — Multi-LLM Bridge for Home Assistant

[![HACS Validation](https://github.com/iAlias/HA-AI-Universal/actions/workflows/hacs.yaml/badge.svg)](https://github.com/iAlias/HA-AI-Universal/actions/workflows/hacs.yaml)
[![Hassfest Validation](https://github.com/iAlias/HA-AI-Universal/actions/workflows/hassfest.yaml/badge.svg)](https://github.com/iAlias/HA-AI-Universal/actions/workflows/hassfest.yaml)

## What it does

HA AI Universal is a Home Assistant custom integration that provides a **universal wrapper** for multiple AI providers. Use a single API to interact with any supported LLM, with automatic fallback if a provider fails.

## Supported Providers

| Provider       | Status |
| -------------- | ------ |
| ChatGPT        | ✅      |
| Gemini         | ✅      |
| Claude         | ✅      |
| Perplexity AI  | ✅      |
| GitHub Copilot | ✅      |

## Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance.
2. Click **Integrations**.
3. Click the three dots in the top right corner and select **Custom repositories**.
4. Add `https://github.com/iAlias/HA-AI-Universal` as an **Integration**.
5. Search for "HA AI Universal" and install it.
6. Restart Home Assistant.

### Manual Installation

1. Download the `custom_components/ha_ai_universal` folder from this repository.
2. Copy it into your Home Assistant `config/custom_components/` directory.
3. Restart Home Assistant.

## Configuration

Set the API key for your preferred provider as an environment variable before starting Home Assistant:

| Variable            | Provider       |
| ------------------- | -------------- |
| `OPENAI_API_KEY`    | ChatGPT        |
| `GEMINI_API_KEY`    | Gemini         |
| `ANTHROPIC_API_KEY` | Claude         |
| `PERPLEXITY_API_KEY`| Perplexity AI  |
| `COPILOT_API_KEY`   | GitHub Copilot |
| `AI_PROVIDER`       | Default provider (default: `openai`) |

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

### Automatic Fallback

If a provider fails, universal-ai automatically tries the next one:

```
ChatGPT → Gemini → Claude → Perplexity → Copilot
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

## License

MIT

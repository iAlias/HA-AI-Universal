# universal-ai

> One API to rule all AIs

**Write once, run on any AI.** A universal wrapper for multiple AI providers.

## Supported Providers

| Provider       | Status |
| -------------- | ------ |
| ChatGPT        | ✅      |
| Gemini         | ✅      |
| Claude         | ✅      |
| Perplexity AI  | ✅      |
| GitHub Copilot | ✅      |

## Quick Start

Install:

```bash
pip install universal-ai
```

Set your API key:

```bash
export OPENAI_API_KEY=your-key-here
```

Use:

```python
from uai import ai

response = ai.ask("Write a REST API in Python")
print(response)
```

## Switch Provider

```python
from uai import ai

ai.use("gemini")
ai.ask("Hello!")
```

Or via environment variable:

```bash
export AI_PROVIDER=gemini
```

## Automatic Fallback

If a provider fails, universal-ai automatically tries the next one:

```
ChatGPT → Gemini → Claude → Perplexity → Copilot
```

## API

```python
ai.ask(prompt)          # generate response
ai.stream(prompt)       # stream response
ai.use("provider")      # switch provider
```

## Environment Variables

| Variable            | Provider       |
| ------------------- | -------------- |
| `OPENAI_API_KEY`    | ChatGPT        |
| `GEMINI_API_KEY`    | Gemini         |
| `ANTHROPIC_API_KEY` | Claude         |
| `PERPLEXITY_API_KEY`| Perplexity AI  |
| `COPILOT_API_KEY`   | GitHub Copilot |
| `AI_PROVIDER`       | Default provider (default: `openai`) |

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

# Providers

## Supported Providers

| Provider       | Module           | API Key Env Variable   |
| -------------- | ---------------- | ---------------------- |
| ChatGPT        | `openai.py`      | `OPENAI_API_KEY`       |
| Gemini         | `gemini.py`      | `GEMINI_API_KEY`       |
| Claude         | `claude.py`      | `ANTHROPIC_API_KEY`    |
| Perplexity AI  | `perplexity.py`  | `PERPLEXITY_API_KEY`   |
| GitHub Copilot | `copilot.py`     | `COPILOT_API_KEY`      |

## Usage

Set the desired provider via environment variable:

```bash
export AI_PROVIDER=openai
```

Or switch at runtime:

```python
from uai import ai

ai.use("gemini")
ai.ask("Hello!")
```

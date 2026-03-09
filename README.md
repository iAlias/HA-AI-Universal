# AI Universal — Home Assistant Expert

A [Home Assistant](https://www.home-assistant.io/) custom integration that acts as a **Home Assistant Expert** by bridging multiple Large Language Model (LLM) providers into a single, unified conversation agent.

Supported providers:
- 🤖 **OpenAI** (ChatGPT / GPT-4o, GPT-4-turbo, GPT-3.5-turbo)
- 🧠 **Anthropic** (Claude 3.5 Sonnet, Claude 3.5 Haiku, Claude 3 Opus)
- ✨ **Google** (Gemini 1.5 Pro, Gemini 1.5 Flash, Gemini 2.0 Flash)
- 🔍 **Perplexity AI** (Llama 3.1 Sonar — with real-time web search)

---

## Features

- **Home Assistant Expert persona** — the AI is pre-prompted with deep Home Assistant knowledge covering automations, YAML configuration, Lovelace dashboards, integrations, templating, and troubleshooting.
- **Multi-turn conversations** — conversation history is maintained per session for context-aware responses.
- **Provider switching** — add multiple entries to compare responses from different providers.
- **Fully customizable** — override the system prompt, max tokens, and temperature via the Options flow.
- **Native conversation agent** — appears in the Home Assistant Assist pipeline alongside other conversation agents.

---

## Requirements

- Home Assistant 2024.1 or later
- An API key from at least one supported provider:
  - [OpenAI API key](https://platform.openai.com/api-keys)
  - [Anthropic API key](https://console.anthropic.com/)
  - [Google AI Studio key](https://aistudio.google.com/app/apikey)
  - [Perplexity API key](https://www.perplexity.ai/settings/api)

---

## Installation

### HACS (recommended)

1. Open **HACS** → **Integrations** → click the ⋮ menu → **Custom repositories**.
2. Add `https://github.com/iAlias/AI-Universal-` with category **Integration**.
3. Search for **AI Universal** and click **Download**.
4. Restart Home Assistant.

### Manual

1. Copy the `custom_components/ai_universal` folder to your Home Assistant `config/custom_components/` directory.
2. Restart Home Assistant.

---

## Setup

1. Go to **Settings** → **Devices & Services** → **Add Integration**.
2. Search for **AI Universal Multi-LLM Bridge**.
3. Select your preferred AI provider (OpenAI, Anthropic, Gemini, or Perplexity).
4. Enter your API key and select the model you want to use.
5. Click **Submit**. The integration validates your key by making a test call.
6. Repeat from step 2 to add additional providers.

### Using the Conversation Agent

Once configured, the AI Universal agent appears as a selectable **Conversation Agent** in:

- **Settings** → **Voice Assistants** → select your assistant → change the **Conversation agent** to *AI Universal (provider)*.
- The **Assist** panel (microphone icon in the sidebar or mobile app).

---

## Options

After setup, click **Configure** on any AI Universal entry to adjust:

| Option | Default | Description |
|---|---|---|
| **System Prompt** | Home Assistant Expert prompt | The AI persona / instructions. Customize to focus on specific topics. |
| **Max Tokens** | 2048 | Maximum length of each response. |
| **Temperature** | 0.7 | Creativity level (0 = deterministic, 2 = very creative). |

---

## Default System Prompt

The integration ships with a **Home Assistant Expert** system prompt that covers:

- Home Assistant YAML configuration (automations, scripts, scenes, helpers)
- Integrations, custom components, and the entity registry
- Smart home protocols (Zigbee, Z-Wave, Matter, Thread, Wi-Fi, Bluetooth)
- Jinja2 templating and Home Assistant expressions
- Lovelace dashboards, custom cards, and themes
- Energy management and long-term statistics
- Security best practices

---

## Contributing

Pull requests and issues are welcome. Please open an issue before starting work on a large feature.

## License

[MIT](LICENSE)

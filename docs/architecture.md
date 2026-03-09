# Architecture

## Overview

universal-ai uses a layered architecture:

```
User
 ↓
AI Router
 ↓
Provider Adapter
 ↓
Provider API
```

## AI Router

The `AIRouter` class is the main entry point. It:

- Selects the active provider
- Manages automatic fallback
- Orchestrates requests

## Adapter Pattern

Every provider implements `BaseProvider` with these methods:

- `generate(prompt)` — generate a text response
- `stream(prompt)` — stream a response token by token
- `healthcheck()` — check if the provider is available

## Fallback

If the active provider fails, the router automatically tries other providers in order until one succeeds.

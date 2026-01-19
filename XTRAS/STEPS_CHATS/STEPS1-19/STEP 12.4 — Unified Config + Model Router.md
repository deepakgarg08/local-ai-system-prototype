**Berlin, Germany — 17 January 2026, 11:31 CET**

Let’s do this carefully. **STEP 12.4** is where policy enters the system — so we keep it **minimal, explicit, and reversible**.

---

# STEP 12.4 — Unified Config + Model Router

## Goal of This Step

Introduce **configuration-driven LLM selection** so that:

* the active LLM backend (local vs online) is chosen by config
* pipelines remain untouched
* all policy lives in **one place**
* failures are explicit and early

This step upgrades the registry from:

> *fixed choice* → *policy-based choice*

---

## What We Will Introduce (and Nothing More)

We will add:

1. A **minimal config module**
2. A **router inside `llms/registry.py`**
3. Environment-variable–based selection (no files parsed yet)

We will **not** add:

* retries
* fallbacks
* priority chains
* agents
* UI or CLI flags

---

## High-Level Shape After STEP 12.4

```
.env
  ↓
configs/runtime.py
  ↓
llms/registry.py   (router)
  ↓
BaseLLM
  ↓
OllamaLLM | OpenAILLM
```

Pipelines still do:

```python
llm = get_llm()
```

---

## 1️⃣ Create the Config Module

### Create folder (if not present)

```
configs/
```

### Create file

```
configs/runtime.py
```

### Contents (copy exactly)

```python
# configs/runtime.py

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class LLMConfig:
    provider: str
    model: str


def load_llm_config() -> LLMConfig:
    """
    Load LLM configuration from environment variables.

    Required variables:
        LLM_PROVIDER: "ollama" or "openai"
        LLM_MODEL: model name for the selected provider
    """
    provider = os.getenv("LLM_PROVIDER")
    model = os.getenv("LLM_MODEL")

    if not provider:
        raise RuntimeError("LLM_PROVIDER is not set")

    if not model:
        raise RuntimeError("LLM_MODEL is not set")

    provider = provider.lower()

    if provider not in {"ollama", "openai"}:
        raise RuntimeError(f"Unsupported LLM_PROVIDER: {provider}")

    return LLMConfig(provider=provider, model=model)
```

Key properties:

* immutable config
* explicit validation
* no defaults
* fail fast

---

## 2️⃣ Update `.env`

Extend your existing `.env`:

```env
# LLM selection
LLM_PROVIDER=ollama
LLM_MODEL=deepseek-coder:6.7b

# Online LLM (only required if provider=openai)
OPENAI_API_KEY=sk-your-key-here
```

Nothing else yet.

---

## 3️⃣ Upgrade the Registry into a Router

### Edit `llms/registry.py`

Replace its contents with this **authoritative version**:

```python
# llms/registry.py

from llms.base import BaseLLM
from llms.ollama import OllamaLLM
from llms.openai import OpenAILLM
from configs.runtime import load_llm_config


def get_llm() -> BaseLLM:
    """
    Unified entry point for obtaining an LLM instance.

    Selection is config-driven and explicit.
    """
    cfg = load_llm_config()

    if cfg.provider == "ollama":
        return OllamaLLM(model=cfg.model)

    if cfg.provider == "openai":
        return OpenAILLM(model=cfg.model)

    # Defensive (should be unreachable)
    raise RuntimeError(f"Unhandled LLM provider: {cfg.provider}")
```

Important:

* routing logic lives **only here**
* no pipelines changed
* adding new providers later is trivial

---

## 4️⃣ Load `.env` (Shell-Level, Same as Before)

```bash
export $(grep -v '^#' .env | xargs)
```

---

## 5️⃣ Verify — Local Path

```bash
python pipelines/llm/test_llm_interface.py
```

Expected:

* Ollama runs
* Uses `deepseek-coder:6.7b`
* No code changes needed

---

## 6️⃣ Verify — Online Path (Optional)

Edit `.env` temporarily:

```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
```

Reload env and run the same test:

```bash
export $(grep -v '^#' .env | xargs)
python pipelines/llm/test_llm_interface.py
```

Same pipeline. Different backend.

That is the **proof** this step worked.

---

## What We Achieved in STEP 12.4

You now have:

* ✅ config-driven LLM selection
* ✅ unified router
* ✅ local + online parity
* ✅ zero pipeline coupling
* ✅ explicit failure modes
* ✅ future-proof extension point

And still:

* ❌ no agents
* ❌ no retries
* ❌ no fallbacks
* ❌ no UI / API

Exactly as intended.

---

## System State Now

```
LLM capabilities:   local + online
Selection method:  env-config
Router present:    yes
Pipelines touched: no
End-to-end RAG:    not yet
```

---

## Next (Final Step in 12)

The only thing left in STEP 12 is:

### **STEP 12.5 — End-to-End RAG Runner (query → answer)**

This will:

* wire retriever + prompt + LLM
* produce a single callable pipeline
* still no UI, no server

When ready, say:

> **“Proceed to STEP 12.5”**

You’re building this exactly the way robust systems are built.

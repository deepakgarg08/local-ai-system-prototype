**Berlin, Germany — 17 January 2026, 11:18 CET**

Let’s proceed cleanly and deliberately.

Below is **STEP 12.3 — Online LLM Integration**, designed to fit **exactly** into the architecture you’ve already established, without refactoring or shortcuts.

---

# STEP 12.3 — Online LLM Integration (OpenAI-style API)

## Goal of This Step

Add a **real online LLM backend** that:

* implements the existing `BaseLLM` interface
* lives alongside `OllamaLLM` as a peer capability
* does **not** affect pipelines
* does **not** introduce routing or config logic yet

At the end of this step:

* the system supports **multiple LLM capabilities**
* but still exposes **only one active LLM** via the registry

---

## Non-Goals (Very Important)

This step explicitly does **not** include:

* switching between local and online models
* config files or env-based selection
* fallback or retries
* agents or tools
* modifying pipelines

Those belong to STEP 12.4+.

---

## Architectural Placement

The new capability will live here:

```
llms/
├── base.py
├── ollama.py
├── registry.py
└── openai.py        ← NEW (this step)
```

`pipelines/` will remain untouched.

---

## Design Contract (Must Hold)

The online LLM must:

* subclass or conform to `BaseLLM`
* expose:

  ```python
  generate(prompt: str) -> str
  ```
* fail loudly on:

  * missing API key
  * network errors
  * API errors

No silent retries. No masking failures.

---

## Step-by-Step Implementation

### 1️⃣ Create the File

Create exactly:

```
llms/openai.py
```

---

### 2️⃣ Implement `OpenAILLM`

Below is a **real, minimal, production-honest implementation** using an OpenAI-style REST API (compatible with OpenAI, Azure-OpenAI, or local OpenAI-compatible servers).

```python
# llms/openai.py

import os
import requests

from llms.base import BaseLLM


class OpenAILLM(BaseLLM):
    """
    Online LLM implementation using an OpenAI-style Chat Completions API.
    """

    def __init__(
        self,
        model: str,
        api_key: str | None = None,
        base_url: str = "https://api.openai.com/v1",
        timeout: int = 60,
    ):
        self.model = model
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is required for OpenAILLM but was not provided."
            )

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def generate(self, prompt: str) -> str:
        url = f"{self.base_url}/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2,
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=self.timeout,
        )

        if response.status_code != 200:
            raise RuntimeError(
                f"OpenAI API error {response.status_code}: {response.text}"
            )

        data = response.json()

        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError) as e:
            raise RuntimeError(
                f"Malformed OpenAI response: {data}"
            ) from e
```

---

### 3️⃣ Do NOT Touch the Registry Yet

At the end of STEP 12.3:

* `llms/registry.py` **still returns `OllamaLLM`**
* online LLM exists but is **not active**
* this is intentional

We are adding **capability**, not **policy**.

---

### 4️⃣ Optional: Manual Smoke Test (Isolated)

You may test this **without involving pipelines**:

```bash
export OPENAI_API_KEY="sk-..."

python - <<'EOF'
from llms.openai import OpenAILLM

llm = OpenAILLM(model="gpt-4o-mini")
print(llm.generate("Explain RAG in one sentence."))
EOF
```

This test is optional but recommended.

---

## What We Achieved in STEP 12.3

After this step, the system has:

* ✅ two real LLM implementations

  * `OllamaLLM` (local)
  * `OpenAILLM` (online)
* ✅ both conforming to the same `BaseLLM`
* ✅ zero pipeline changes
* ✅ zero routing logic
* ✅ full failure transparency

This **proves** your abstraction is correct.

---

## System State After STEP 12.3

```
LLM capabilities:      local + online
Active backend:        local only
Unified interface:     yes
Routing / config:      no
End-to-end RAG:        no
```

This is the **only safe intermediate state**.

---

## What Comes Next

The next logical step is:

### 👉 **STEP 12.4 — Unified Config + Model Router**

This is where:

* `registry.py` gains selection logic
* configs/env decide which LLM is active
* pipelines still remain untouched

When ready, say:

> **“Proceed to STEP 12.4 — Unified Config + Model Router”**

You’re building this exactly the right way.

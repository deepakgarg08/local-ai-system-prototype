**📅 Friday, 16 January 2026, 23:09 (Berlin time)**

Excellent.
We now enter the **most important architectural phase** of STEP 12.1:

# ✅ Phase 3 — `BaseLLM` Interface + `OllamaLLM` Implementation

This phase **locks the contract** that *all future LLMs* (online, agents, tools) will obey.

---

## Phase 3 — Objective (Non-Negotiable)

By the end of this phase:

* ✅ One **abstract LLM interface**
* ✅ One **real Ollama-backed implementation**
* ✅ Zero RAG
* ✅ Zero agents
* ✅ Zero routing logic
* ✅ Clean separation between **interface** and **vendor**

---

## Folder Placement (Final for STEP 12)

Create this inside your project root:

```text
llms/
├── __init__.py
├── base.py        ← abstract contract
└── ollama.py     ← real implementation
```

This folder will **never import RAG, FAISS, or agents**.

---

## 1️⃣ `llms/base.py` — The LLM Contract

This is the **single most important file** so we keep it minimal.

```python
# llms/base.py
from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    Abstract base class for all LLM backends.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a completion for a given prompt.

        Args:
            prompt (str): Input prompt

        Returns:
            str: Model-generated text
        """
        raise NotImplementedError
```

### Why this is correct

* no vendor assumptions
* no message format yet
* no streaming yet
* no tool calls yet

➡️ Everything else adapts *to this*.

---

## 2️⃣ `llms/ollama.py` — Real Local Implementation

```python
# llms/ollama.py
from ollama import chat
from llms.base import BaseLLM


class OllamaLLM(BaseLLM):
    def __init__(self, model: str):
        self.model = model

    def generate(self, prompt: str) -> str:
        response = chat(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response["message"]["content"]
```

### Key design decisions

* Uses **official Ollama client**
* No hardcoded model
* No retries yet
* No logging yet

This is **pure correctness**.

---

## 3️⃣ Smoke Test (MANDATORY)

Create a temporary test file:

```bash
nano test_llm_interface.py
```

```python
from llms.ollama import OllamaLLM

llm = OllamaLLM(model="deepseek-coder:6.7b")

response = llm.generate(
    "Explain what a vector database is in one concise paragraph."
)

print(response)
```

Run:

```bash
python test_llm_interface.py
```

---

## Success Criteria ✅

You must see:

* a valid paragraph
* no stack traces
* no warnings
* no imports leaking outside `llms/`

If this works → **STEP 12.1 is architecturally complete**.

---

## Why This Phase Is a Big Deal

You now have:

```
BaseLLM
   ↑
OllamaLLM
```

Which means:

* OpenAI-style APIs will be trivial
* Model router becomes config-only
* Agents (later) plug in cleanly
* Testing becomes deterministic

You avoided:

* LangChain lock-in
* premature agent complexity
* hidden side effects

---

## What Comes Next (Preview)

➡️ **STEP 12.2 — Unified LLM Interface**

* add OpenAI-compatible backend
* same `generate()` method
* config-driven selection

---

### 🚦 Stop Point

Run the smoke test and confirm:

> **“Phase 3 passed”**

If you hit *any* error, paste it verbatim and we fix it cleanly.

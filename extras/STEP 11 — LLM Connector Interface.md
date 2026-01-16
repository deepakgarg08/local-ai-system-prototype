**🕒 16 January 2026, 22:55 (Berlin, CET)**

Perfect.
Now we move to **STEP 11 — LLM Connector Interface (local + online)**.
This is a **core architectural step**, so we’ll do it cleanly and future-proof.

---

# STEP 11 — LLM Connector Interface

## 🎯 Goal of Step 11

Create a **single, stable interface** that:

* Accepts the **assembled prompt** (from Step 10)
* Can call:

  * ✅ Local LLMs (later: llama.cpp, vLLM, Ollama, etc.)
  * ✅ Online LLMs (OpenAI, Anthropic, any API)
* Keeps **zero coupling** with prompt assembly or retrieval
* Allows easy swapping of models without touching pipeline logic

---

## 🧠 Design Principle (Very Important)

We use the **Adapter Pattern**.

```
Prompt (string)
   ↓
LLM Interface (abstract)
   ↓
Concrete Adapter
   ├── Local LLM
   └── Online LLM
```

The rest of your system **never knows** which model is used.

---

## 📁 Folder Structure (New)

```
pipelines/
└── llm/
    ├── __init__.py
    ├── base.py          ← abstract interface
    ├── local.py         ← local LLM adapter (stub for now)
    └── online.py        ← online LLM adapter (stub for now)
```

We will **not** connect real models yet — only the interface.

---

## 1️⃣ Base Interface (`base.py`)

This defines the **contract** every LLM must follow.

```python
# pipelines/llm/base.py

from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    Abstract base class for all LLM connectors.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response for the given prompt.

        Parameters
        ----------
        prompt : str
            Fully assembled prompt

        Returns
        -------
        str
            Model-generated response
        """
        pass
```

✔ simple
✔ enforceable
✔ extensible

---

## 2️⃣ Local LLM Adapter (`local.py`)

This is a **placeholder** for now.

Later this will connect to:

* llama.cpp
* Ollama
* vLLM
* text-generation-webui

```python
# pipelines/llm/local.py

from .base import BaseLLM


class LocalLLM(BaseLLM):
    """
    Adapter for local LLMs.
    """

    def __init__(self, model_name: str = "local-model"):
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        # TODO: replace with actual local inference
        return (
            "[LOCAL LLM PLACEHOLDER RESPONSE]\n\n"
            f"Prompt received ({len(prompt)} characters)."
        )
```

---

## 3️⃣ Online LLM Adapter (`online.py`)

Also a **stub**, but designed for APIs.

```python
# pipelines/llm/online.py

from .base import BaseLLM


class OnlineLLM(BaseLLM):
    """
    Adapter for online LLM APIs (OpenAI, Anthropic, etc.).
    """

    def __init__(self, provider: str = "generic"):
        self.provider = provider

    def generate(self, prompt: str) -> str:
        # TODO: replace with actual API call
        return (
            "[ONLINE LLM PLACEHOLDER RESPONSE]\n\n"
            f"Provider: {self.provider}\n"
            f"Prompt length: {len(prompt)} characters."
        )
```

---

## 4️⃣ Package Export (`llm/__init__.py`)

```python
from .base import BaseLLM
from .local import LocalLLM
from .online import OnlineLLM

__all__ = ["BaseLLM", "LocalLLM", "OnlineLLM"]
```

Now you can import cleanly:

```python
from pipelines.llm import LocalLLM, OnlineLLM
```

---

## 5️⃣ End-to-End Test (Prompt → LLM)

Create a small runner to verify everything is wired correctly.

### 📁 File

```
pipelines/llm/test_llm.py
```

### ✍️ Code

```python
from pipelines.prompting import assemble_prompt
from pipelines.llm import LocalLLM, OnlineLLM


def main():
    query = "What is cosine similarity?"

    context_chunks = [
        {
            "text": "Cosine similarity measures the cosine of the angle between two vectors.",
            "source": "nlp_basics.pdf",
            "chunk_id": 12,
        }
    ]

    prompt = assemble_prompt(query, context_chunks)

    local_llm = LocalLLM()
    online_llm = OnlineLLM(provider="openai")

    print("=== LOCAL LLM ===")
    print(local_llm.generate(prompt))

    print("\n=== ONLINE LLM ===")
    print(online_llm.generate(prompt))


if __name__ == "__main__":
    main()
```

### ▶️ Run from project root

```bash
uv run python pipelines/llm/test_llm.py
```

---

## 🧠 Why This Architecture Is Strong

✔ prompt logic isolated
✔ retrieval logic isolated
✔ model logic isolated
✔ supports **multiple providers simultaneously**
✔ zero refactor when switching models
✔ aligns with enterprise RAG systems

This is **exactly how large production systems are built**.

---

## ✅ STEP 11 STATUS

| Component             | Status   |
| --------------------- | -------- |
| LLM interface         | ✅        |
| Local adapter         | ✅ (stub) |
| Online adapter        | ✅ (stub) |
| Prompt compatibility  | ✅        |
| Ready for real models | ✅        |

---

## 🔜 What Comes Next (Choose)

You can now choose the next direction:

1️⃣ **STEP 12 — Real Local LLM Integration (Ollama / llama.cpp)**
2️⃣ **STEP 12 — Real Online LLM Integration (OpenAI-style API)**
3️⃣ **STEP 12 — Unified Config + Model Router**
4️⃣ **STEP 12 — End-to-End RAG Runner (query → answer)**

Just tell me **which one** and we’ll continue cleanly.

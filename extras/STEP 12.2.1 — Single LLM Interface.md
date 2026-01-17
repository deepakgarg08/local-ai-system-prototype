**Berlin, Germany — 16 January 2026, 22:58 (CET)**

Below is a **clean, end-to-end summary of STEP 12.2 — Unified LLM Interface**, **exactly aligned with your current working system**, including:

* ✅ what the goal is
* ✅ which files to create
* ✅ where to put them
* ✅ the **final code** (minimal, production-safe)
* ✅ what changes and what does NOT change

No future features, no speculation.

---

# STEP 12.2 — Single LLM Interface

**(Summary + File Generation + Code)**

---

## 1️⃣ Goal of STEP 12.2 (Very Precise)

> Replace the **direct Ollama call** with a **stable abstraction**,
> without changing system behavior.

After this step:

* Your pipeline still works exactly the same
* But the system no longer “knows” it’s using Ollama
* Any LLM (local or API) can be swapped later

This is a **refactor**, not a feature.

---

## 2️⃣ What Already Exists (Baseline)

You already have this working pipeline:

```
run_query.py
  ↓
retriever.py        (FAISS, disk-backed)
  ↓
prompt_builder.py
  ↓
llm_ollama.py       ❌ (to be refactored)
```

We will **replace only the LLM part**.

---

## 3️⃣ New Files to Create (Exact Locations)

Create a new folder:

```
pipelines/llm/
```

Inside it, create **3 files**:

```bash
mkdir -p pipelines/llm

touch \
pipelines/llm/__init__.py \
pipelines/llm/base.py \
pipelines/llm/ollama.py \
pipelines/llm/factory.py
```

---

## 4️⃣ File-by-File Code (Final Versions)

### 📄 `pipelines/llm/base.py`

**The contract (interface)**

```python
from abc import ABC, abstractmethod


class BaseLLM(ABC):
    @abstractmethod
    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> str:
        """
        Generate text from a prompt.
        Must return plain text.
        """
        raise NotImplementedError
```

---

### 📄 `pipelines/llm/ollama.py`

**Concrete Ollama adapter (logic moved here)**

```python
import requests
from pipelines.llm.base import BaseLLM


class OllamaLLM(BaseLLM):
    def __init__(
        self,
        model: str,
        base_url: str = "http://localhost:11434",
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")

    def generate(
        self,
        prompt: str,
        *,
        temperature: float = 0.2,
        max_tokens: int | None = None,
    ) -> str:
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "options": {
                    "temperature": temperature,
                },
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()
        data = response.json()

        return data["message"]["content"]
```

✔ Same API you already tested
✔ Same behavior
✔ Just moved behind an interface

---

### 📄 `pipelines/llm/factory.py`

**Single place that decides which LLM is used**

```python
from pipelines.llm.ollama import OllamaLLM


def load_llm():
    """
    Temporary hard-coded factory.
    Will become config-driven later.
    """
    return OllamaLLM(
        model="deepseek-coder-tuned:latest"
    )
```

---

## 5️⃣ Update Existing File (Very Small Change)

### 📄 `pipelines/query/run_query.py`

#### ❌ Old import

```python
from pipelines.query.llm_ollama import run_ollama
```

#### ✅ New imports

```python
from pipelines.llm.factory import load_llm
```

---

### Replace `answer_query` with this

```python
def answer_query(query: str) -> str:
    contexts = retrieve_context(query)
    prompt = build_prompt(query, contexts)

    llm = load_llm()
    return llm.generate(prompt)
```

That’s it.

No other file changes.

---

## 6️⃣ What Did NOT Change (Important)

* ❌ Retrieval logic
* ❌ FAISS index
* ❌ Prompt format
* ❌ Ollama behavior
* ❌ How you run the system

You still run:

```bash
uv run python -m pipelines.query.run_query
```

---

## 7️⃣ What You Achieved by STEP 12.2

After this step, your system has:

* ✅ End-to-end RAG
* ✅ Disk-backed retrieval
* ✅ Local LLM inference
* ✅ **LLM abstraction layer**
* ✅ Zero vendor lock-in
* ✅ Safe foundation for future features

This is a **major architectural milestone**.

---

## 8️⃣ Clear Boundary: What Comes After (Not Now)

Deferred (as you requested):

* Reranking / MMR
* Hybrid BM25
* Tools / function calling
* Agents
* Streaming
* UI

Those now sit **on top of a stable core**.

---

## 9️⃣ One-Sentence Summary

> **STEP 12.2 cleanly replaces a hard-coded Ollama call with a Unified LLM Interface, without changing system behavior.**

If you want next, we can:

* Freeze this with a small test
* Make the factory config-driven
* Or document this step under `docs/steps/`

Just tell me the next move.

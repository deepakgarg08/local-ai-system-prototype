**🕒 16 January 2026, 22:31 (Berlin, CET)**

## STEP 10 — Prompt Assembly ✅

Let’s proceed in a **clean, production-grade way**, aligned with your Fedora-based local AI system and what we’ve already built.

At this step, we **do NOT call any LLM yet**.
We only **assemble the final prompt** that *will later* be sent to any LLM (local or online).

---

## 🎯 Goal of Step 10

Convert:

* **User query**
* **Retrieved context chunks (from FAISS / cosine similarity)**

into a **single structured prompt string** that:

* Is deterministic
* Is model-agnostic
* Can be reused for **local LLMs** or **online APIs** later

---

## 📌 Inputs to Prompt Assembly

At runtime, Step 10 receives:

1. **User Query**

```text
"What is cosine similarity?"
```

2. **Retrieved Context Chunks**

```python
[
  {
    "text": "...",
    "source": "doc1.pdf",
    "chunk_id": 3
  },
  {
    "text": "...",
    "source": "doc2.txt",
    "chunk_id": 7
  }
]
```

3. **Optional System Instruction**

```text
"You are a precise technical assistant. Answer only from the provided context."
```

---

## 🧠 Prompt Design (Very Important)

We use a **3-part prompt** (this is deliberate and scalable):

### 1️⃣ System Instruction

Sets behavior and constraints.

### 2️⃣ Context Block

All retrieved chunks, clearly separated and labeled.

### 3️⃣ User Question

The actual question to answer.

This structure:

* Works for **LLaMA, Mistral, DeepSeek, GPT, Claude**
* Avoids hallucination
* Keeps reasoning grounded

---

## 🧱 Prompt Template (Canonical)

Here is the **exact logical template** we will implement:

```
SYSTEM:
<system_instruction>

CONTEXT:
[1] <chunk text>
[2] <chunk text>
...

QUESTION:
<user query>

INSTRUCTIONS:
- Answer only using the CONTEXT above
- If the answer is not present, say "I don't know"
- Be concise and precise
```

---

## 🗂️ Where This Lives in the Project

We now **introduce a new file** (conceptually; you asked for explanation, not file creation yet):

```
pipelines/
└── prompting/
    └── assemble_prompt.py
```

This keeps:

* Retrieval logic ❌ separate
* LLM calling ❌ separate
* Prompt logic ✅ isolated and testable

---

## 🧩 Core Logic (Conceptual Python)

```python
def assemble_prompt(
    query: str,
    context_chunks: list[dict],
    system_instruction: str | None = None
) -> str:
    system_instruction = system_instruction or (
        "You are a helpful assistant. Use only the provided context."
    )

    context_block = ""
    for i, chunk in enumerate(context_chunks, start=1):
        context_block += f"[{i}] {chunk['text']}\n\n"

    prompt = f"""
SYSTEM:
{system_instruction}

CONTEXT:
{context_block}

QUESTION:
{query}

INSTRUCTIONS:
- Answer only using the CONTEXT above
- If the answer is not present, say "I don't know"
- Be concise and precise
""".strip()

    return prompt
```

⚠️ **No embeddings, no FAISS, no LLM here**
This is pure string assembly.

---

## 🧪 Example Output (What Step 10 Produces)

```
SYSTEM:
You are a precise technical assistant. Answer only from the provided context.

CONTEXT:
[1] Cosine similarity measures the cosine of the angle between two vectors...

[2] It is commonly used in information retrieval and NLP...

QUESTION:
What is cosine similarity?

INSTRUCTIONS:
- Answer only using the CONTEXT above
- If the answer is not present, say "I don't know"
- Be concise and precise
```

This string is the **final artifact of Step 10**.

---

## 🔌 Why This Matters for Later Steps

Because of Step 10:

* You can plug in **any LLM** later
* You can unit-test prompts without models
* You can log, cache, diff prompts
* You can support **offline + online LLMs** cleanly

---

## ✅ Step 10 Status

| Aspect                       | Status        |
| ---------------------------- | ------------- |
| Prompt design                | ✅ Final       |
| Model-agnostic               | ✅             |
| LangChain-free               | ✅ (by design) |
| Ready for online LLM adapter | ✅             |
| Fedora / local-first aligned | ✅             |

---


**🕒 16 January 2026, 22:38 (Berlin, CET)**

Perfect — now we **actually implement STEP 10** in code, cleanly and minimally, exactly matching what we designed.

We will:

* Add a **new prompting module**
* Keep it **pure Python**
* Keep it **LLM-agnostic**
* Make it **testable and reusable**

No LangChain, no model calls.

---

## ✅ STEP 10 — Prompt Assembly (Implementation)

### 📁 Target location in your project

```
pipelines/
└── prompting/
    ├── __init__.py
    └── assemble_prompt.py
```

---

## 1️⃣ `pipelines/prompting/assemble_prompt.py`

```python
# pipelines/prompting/assemble_prompt.py

from typing import List, Dict, Optional


DEFAULT_SYSTEM_INSTRUCTION = (
    "You are a precise technical assistant. "
    "Answer only using the provided context. "
    "Do not use outside knowledge."
)


def assemble_prompt(
    query: str,
    context_chunks: List[Dict],
    system_instruction: Optional[str] = None,
) -> str:
    """
    Assemble the final prompt string for an LLM.

    Parameters
    ----------
    query : str
        User question
    context_chunks : List[Dict]
        Retrieved chunks from vector search.
        Each dict must contain at least a 'text' field.
    system_instruction : Optional[str]
        Optional system-level instruction.

    Returns
    -------
    str
        Fully assembled prompt
    """

    system_instruction = system_instruction or DEFAULT_SYSTEM_INSTRUCTION

    if not context_chunks:
        context_block = "No relevant context was retrieved."
    else:
        context_block_lines = []
        for idx, chunk in enumerate(context_chunks, start=1):
            text = chunk.get("text", "").strip()
            source = chunk.get("source", "unknown")
            chunk_id = chunk.get("chunk_id", "n/a")

            context_block_lines.append(
                f"[{idx}] (source: {source}, chunk: {chunk_id})\n{text}"
            )

        context_block = "\n\n".join(context_block_lines)

    prompt = f"""
SYSTEM:
{system_instruction}

CONTEXT:
{context_block}

QUESTION:
{query}

INSTRUCTIONS:
- Answer only using the CONTEXT above
- If the answer is not present, say "I don't know"
- Be concise and precise
""".strip()

    return prompt
```

---

## 2️⃣ `pipelines/prompting/__init__.py`

```python
from .assemble_prompt import assemble_prompt
```

This allows:

```python
from pipelines.prompting import assemble_prompt
```

---

## 3️⃣ Example Usage (Integration Test)

This is **not production code**, just a sanity check:

```python
from pipelines.prompting import assemble_prompt

query = "What is cosine similarity?"

context_chunks = [
    {
        "text": "Cosine similarity measures the cosine of the angle between two vectors.",
        "source": "nlp_basics.pdf",
        "chunk_id": 12,
    },
    {
        "text": "It is commonly used in information retrieval and NLP tasks.",
        "source": "search_notes.txt",
        "chunk_id": 4,
    },
]

prompt = assemble_prompt(query, context_chunks)

print(prompt)
```

---

## 4️⃣ Output (What Step 10 Produces)

```
SYSTEM:
You are a precise technical assistant. Answer only using the provided context. Do not use outside knowledge.

CONTEXT:
[1] (source: nlp_basics.pdf, chunk: 12)
Cosine similarity measures the cosine of the angle between two vectors.

[2] (source: search_notes.txt, chunk: 4)
It is commonly used in information retrieval and NLP tasks.

QUESTION:
What is cosine similarity?

INSTRUCTIONS:
- Answer only using the CONTEXT above
- If the answer is not present, say "I don't know"
- Be concise and precise
```

This string is the **final artifact of STEP 10**.

---

## 🧠 Why This Implementation Is Correct

✔ Deterministic
✔ No dependency on FAISS, embeddings, or models
✔ Handles empty context safely
✔ Explicit source metadata (debugging + trust)
✔ Ready for **local LLMs** and **online APIs**

---

## ✅ STEP 10 — COMPLETE

At this point your pipeline looks like:

```
User Query
   ↓
Embedding
   ↓
FAISS (cosine similarity)
   ↓
Retrieved Chunks
   ↓
STEP 10: Prompt Assembly  ✅
   ↓
(Next) LLM Connector
```

---

When you’re ready, say:

**“Proceed to STEP 11 — LLM Connector Interface (local + online)”**

That’s where we wire this prompt into **any model you want**.

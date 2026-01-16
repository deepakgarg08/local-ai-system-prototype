**🕒 16 January 2026, 18:12 (Berlin, Germany)**

Great — we’ll **proceed with STEP 7b: Retrieval → Prompt Assembly (citations & context window)**.
This step is purely **orchestration logic** on top of what you already have (chunks + embeddings + retrieval). No model changes yet.

Below is a **clean, implementation-ready design**, aligned with your **Fedora 43 / local LLM / RAG prototype**.

---

## STEP 7b — Retrieval → Prompt Assembly

**Goal:**
Turn retrieved chunks into a **deterministic, citation-aware prompt** that fits the model’s context window and produces grounded answers.

---

## 1. Inputs & Outputs

### Inputs

* `query: str` – user question
* `retrieved_chunks: List[Chunk]` – output of vector search (STEP 7a later refines scoring)
* `max_context_tokens: int` – model limit (e.g. DeepSeek 6B ≈ 4k–8k)
* `system_prompt: str` – fixed RAG instruction

### Output

* `final_prompt: str` – passed to local LLM
* `citations_map: Dict[int, ChunkMetadata]` – for post-answer attribution

---

## 2. Chunk Data Contract (important)

Every retrieved chunk **must** carry metadata like this:

```python
{
  "chunk_id": "sec_03_chunk_02",
  "source": "document_name.pdf",
  "section": "3.2 Architecture Overview",
  "page": 14,
  "text": "The actual chunk content...",
  "score": 0.82
}
```

This metadata is **non-negotiable** if you want citations.

---

## 3. Prompt Structure (Canonical)

Your final prompt should always follow this structure:

```
[SYSTEM INSTRUCTIONS]

[CONTEXT BLOCK WITH CITED CHUNKS]

[USER QUESTION]

[ANSWERING RULES]
```

This consistency is what keeps local LLMs stable.

---

## 4. System Prompt (RAG-safe)

```text
You are a precise technical assistant.
Answer ONLY using the provided context.
If the answer is not contained in the context, say:
"I don’t have enough information to answer that."

Cite facts using [n] notation, where n refers to the context chunk number.
Do not invent sources.
```

Keep this **short and strict** — local models follow rules better when concise.

---

## 5. Context Assembly with Citations

### Numbered context blocks

```text
### Context

[1] (source: docA.pdf, section: 2.1, page: 5)
Chunk text here...

[2] (source: docB.pdf, section: 4.3, page: 18)
Chunk text here...
```

### Why numbering matters

* Enables **inline citations**
* Lets you map `[2]` → exact PDF + page later
* Simplifies evaluation & debugging

---

## 6. Token-Budgeted Context Packing

You **must not blindly concatenate chunks**.

### Strategy

1. Sort chunks by:

   * score (desc)
   * shorter chunks first (better packing)
2. Add chunks until token limit reached
3. Leave ~20–25% buffer for answer generation

### Example

```python
MAX_CONTEXT_TOKENS = 3000
BUFFER = 800
budget = MAX_CONTEXT_TOKENS - BUFFER
```

Stop adding chunks once `budget` is exceeded.

---

## 7. Prompt Builder (Minimal Code)

```python
def build_prompt(query, chunks):
    context_blocks = []
    citations = {}

    for i, ch in enumerate(chunks, start=1):
        context_blocks.append(
            f"[{i}] (source: {ch['source']}, "
            f"section: {ch['section']}, page: {ch['page']})\n"
            f"{ch['text']}"
        )
        citations[i] = ch

    context_text = "\n\n".join(context_blocks)

    prompt = f"""
You are a precise technical assistant.
Answer ONLY using the provided context.
Cite facts using [n].

### Context
{context_text}

### Question
{query}

### Answer
"""

    return prompt.strip(), citations
```

This is **STEP-7b complete logic**.

---

## 8. Expected Model Output

```text
The system uses a vector database to store embeddings for retrieval [1].
Chunking is performed at the section level to preserve semantic coherence [2].
```

Post-processing can now:

* Extract `[1]`, `[2]`
* Render proper citations in UI / CLI / API response

---

## 9. What STEP 7b Does *NOT* Do

❌ No reranking
❌ No score thresholds
❌ No embedding decisions
❌ No model tuning

Those belong to:

* **STEP 7a** → retrieval strategy & scoring
* **STEP 6c** → embeddings + backend

---

## 10. You’re Now Ready For

**Next logical steps (your choice later):**

* STEP 7a — hybrid scoring + reranker
* Answer post-processing (citation formatting)
* Streaming answers from local DeepSeek
* Evaluation harness (gold Q/A)

---

If you want, next I can:

* 🔹 Add **exact token counting** (tiktoken-style)
* 🔹 Show **CLI output formatting with citations**
* 🔹 Integrate this directly into your existing pipeline structure

Just say the word.


.................

**🕒 16 January 2026, 18:18 (Berlin, Germany)**

Short answer: **YES — STEP 7b *should* have its own file implementation**, even though it’s mostly orchestration.

Below is the **clean, minimal, production-grade answer** tailored to your current repo style.

---

## Why STEP 7b deserves its own file

STEP 7b is **not just glue code**. It is responsible for:

* Deterministic prompt construction
* Context window enforcement
* Citation numbering & mapping
* Model-agnostic prompt format

This logic **will evolve**, so isolating it now is the correct move.

---

## Recommended File Placement

```text
pipelines/
├── retrieval/
│   ├── search.py          # vector search (STEP 7a later)
│   └── scoring.py         # thresholds / reranking (STEP 7a)
│
├── prompting/
│   ├── prompt_builder.py  # ✅ STEP 7b (THIS FILE)
│   └── system_prompts.py  # fixed system instructions
│
├── llm/
│   └── local_llm.py       # DeepSeek invocation
```

This keeps **retrieval ≠ prompting ≠ generation** cleanly separated.

---

## STEP 7b — `prompt_builder.py` (Canonical)

### `pipelines/prompting/prompt_builder.py`

```python
from typing import List, Dict, Tuple

def build_prompt(
    query: str,
    chunks: List[Dict],
    max_context_tokens: int = 3000,
    buffer_tokens: int = 800,
) -> Tuple[str, Dict[int, Dict]]:
    """
    Build a citation-aware prompt from retrieved chunks.

    Returns:
        prompt (str)
        citations (dict[int, chunk_metadata])
    """

    budget = max_context_tokens - buffer_tokens
    used_tokens = 0

    context_blocks = []
    citations = {}

    for i, ch in enumerate(chunks, start=1):
        text = ch["text"]
        token_estimate = len(text.split())  # replace later with tokenizer

        if used_tokens + token_estimate > budget:
            break

        block = (
            f"[{i}] (source: {ch['source']}, "
            f"section: {ch['section']}, page: {ch['page']})\n"
            f"{text}"
        )

        context_blocks.append(block)
        citations[i] = ch
        used_tokens += token_estimate

    context_text = "\n\n".join(context_blocks)

    prompt = f"""
You are a precise technical assistant.
Answer ONLY using the provided context.
If the answer is not in the context, say so.
Cite facts using [n].

### Context
{context_text}

### Question
{query}

### Answer
""".strip()

    return prompt, citations
```

This file **is STEP 7b**. Nothing more, nothing less.

---

## What imports this file?

Example:

```python
from pipelines.prompting.prompt_builder import build_prompt

prompt, citations = build_prompt(query, retrieved_chunks)

response = local_llm.generate(prompt)
```

---

## What STEP 7b owns (clearly defined)

✅ Prompt structure
✅ Context packing
✅ Citation mapping
✅ Token budgeting

---

## What STEP 7b does NOT own

❌ Vector search
❌ Score thresholds
❌ Reranking
❌ Model inference

Those are separate steps by design.

---

## Verdict (clear answer)

✔ **YES — STEP 7b has a real file**
✔ It should live under `pipelines/prompting/`
✔ It is stable, testable, and reusable
✔ You are correct to implement it now

---

If you want next, I can:

* Add **unit tests** for `prompt_builder.py`
* Upgrade token counting to **real tokenizer**
* Show **how to extract citations from model output**
* Wire it directly into your current CLI pipeline

Just tell me the next step.

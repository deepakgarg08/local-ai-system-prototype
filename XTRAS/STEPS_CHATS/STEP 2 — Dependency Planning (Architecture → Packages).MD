**📅 14 January 2026, 17:38 (Berlin time)**

Excellent. You are now in a **very good professional state**:

* Python **3.11.14**
* Conda-managed environment
* `uv 0.9.24`
* Clean repo
* No dependency debt yet

Now we do **dependency planning only** — no installs (except `uv`, which is already done).

---

# STEP 2 — Dependency Planning (Architecture → Packages)

## Goal of this step

Define **what categories of libraries exist**, **why they exist**, and **what is explicitly NOT installed yet**.

This prevents:

* dependency sprawl
* random installs
* broken environments

---

## 1. Dependency Layers (High-Level)

We split dependencies into **strict layers**:

```
A. Core & Runtime
B. Data Ingestion & Parsing
C. Text Processing & Chunking
D. Embeddings
E. Vector Storage
F. LLM Inference
G. Application & Interface
H. Utilities & Tooling
```

Each layer will be introduced **only when needed**.

---

## 2. What We Install NOW (Minimum Viable)

### A. Core & Runtime (MANDATORY)

| Purpose         | Why                         |
| --------------- | --------------------------- |
| `rich`          | structured logs & debugging |
| `pydantic`      | data validation & schemas   |
| `python-dotenv` | env config                  |
| `loguru`        | clean logging               |

➡️ These are **not AI-specific**, safe, and low risk.

---

## 3. What We Explicitly Delay (IMPORTANT)

### 🚫 Not installing yet:

* ❌ PyTorch
* ❌ Transformers
* ❌ Sentence transformers
* ❌ FAISS / Chroma / Milvus
* ❌ LangChain / LlamaIndex
* ❌ FastAPI / Gradio / Streamlit

Reason:

> Until we finalize **data flow**, these choices are premature.

---

## 4. Planned Dependencies (Not Installed Yet)

### B. Data Ingestion & Parsing (Later)

* PDF parsers
* DOCX / PPTX readers
* Image OCR (optional)

### C. Chunking & Metadata

* Tokenizers
* Text splitters

### D. Embeddings

* Lightweight embedding model libs

### E. Vector Stores

* Local disk-based DB

### F. LLM

* Local inference runtime

### G. App Layer

* CLI or simple UI

---

## 5. Create `requirements.in` (Intent File)

Now we **write intent, not installs**.

From project root:

```bash
nano requirements.in
```

Add:

```text
# Core runtime
rich
pydantic
python-dotenv
loguru
```

Save.

---

## 6. Compile Locked Requirements (uv)

Now we **lock versions deterministically**.

```bash
uv pip compile requirements.in -o requirements.txt
```

This generates:

* fully resolved versions
* hashes
* reproducible installs

---

## 7. Install ONLY These Core Dependencies

```bash
uv pip install -r requirements.txt
```

This is safe and intentional.

---

## 8. Verify Environment Health

Quick check:

```bash
python - << 'EOF'
from rich import print
from pydantic import BaseModel
from loguru import logger

print("[green]Dependency planning successful[/green]")
logger.info("Logging works")
EOF
```

---

## 9. Commit This Step

```bash
git add requirements.in requirements.txt
git commit -m "Add core runtime dependencies and lockfile"
```

---

## 10. Why This Matters (Big Picture)

You now have:

* A **stable foundation**
* Deterministic installs
* A clear growth path
* Zero AI complexity yet

This mirrors how **real AI systems are built**, including those described in your PDF .

---

## Next Step (I recommend)

👉 **Next: Sample Data Layout**

Why:

* Everything in this system is driven by data
* We need realistic but tiny inputs
* This unlocks ingestion & chunking next

If you agree, reply:

> **“Next: sample data layout”**

We’ll continue cleanly.

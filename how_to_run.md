**Berlin, Germany — 20 January 2026, 20:33 CET**

Good catch — and thanks for the clarification 👍
You’re right: **`uv` is the package / environment manager**, and the `run.md` should reflect that.

### What I attempted

I tried to **surgically update the existing `run.md` in the canvas** to:

* replace `python -m venv` → `uv venv`
* replace `pip install` → `uv pip install`
* mark `uv` explicitly in the **TL;DR** and **Environment Setup** sections

The automated patch failed due to regex matching issues in the canvas tool (nothing you did wrong).

---

## What you should do (simple & safe)

Please make the following **manual edits** in `run.md`.
These are **exact replacements** and keep the document fully STEP 20.9-compatible.

---

### 1️⃣ TL;DR — Quick Start (replace entire block)

```bash
# 1. Create & activate virtual environment (uv)
uv venv .venv
source .venv/bin/activate

# 2. Install dependencies (uv)
uv pip install -r requirements.txt

# 3. Configure LLM (example: local Ollama)
export LLM_PROVIDER=ollama
export LLM_MODEL=llama3

# 4. Build index (one-time, offline)
python -m pipelines.indexing.build_index

# 5. Run a local test query (recommended entry point)
python scripts/run_query.py
```

---

### 2️⃣ Section 3.1 — Create a Virtual Environment

Change heading and commands to:

````md
### 3.1 Create a Virtual Environment (uv)

```bash
uv venv .venv
source .venv/bin/activate
````

````

---

### 3️⃣ Section 3.2 — Install Dependencies

Change to:

```md
### 3.2 Install Dependencies (uv)

```bash
uv pip install -r requirements.txt
````

(or `uv pip install -e .` if using `pyproject.toml`)

```

---

## Why this is the **correct final state**

- ✅ Matches your actual tooling (`uv`)
- ✅ Faster, reproducible installs
- ✅ Clear to reviewers / auditors
- ✅ Still purely **runtime-agnostic**
- ✅ No architectural or freeze violations

---

## One-line confirmation (for STEP 20.9)

> Dependency management and virtual environments are handled via **uv**, with `scripts/run_query.py` as the local execution entry point.

If you want, next I can:
- re-emit the **full corrected `run.md`** as a single paste
- add a **CI-friendly uv section**
- or add a **“Why uv” rationale** for reviewers
```

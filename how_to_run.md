**Berlin, Germany — 21 January 2026, 13:22 CET**
## Overview

This project can be run in **two supported ways**:

1. **Local (uv-based)** — for development and debugging
2. **Docker (recommended)** — for reproducible, deployment-like execution

Both use the **same codebase and architecture**.

---

## TL;DR — Quick Start (Docker – Recommended)

```bash
# 1. Build base image (dependencies)
docker build -f docker/Dockerfile.base -t rag-base .

# 2. Build all runtime images
docker compose build

# 3. Build the vector index (offline, one-time or on data change)
docker compose --profile index run --rm rag-indexer

# 4. Run CLI interface
docker compose run --rm rag-runtime
```

---

## TL;DR — Quick Start (Local / uv)

```bash
# 1. Create & activate virtual environment
uv venv .venv
source .venv/bin/activate

# 2. Install dependencies
uv pip install -e .

# 3. Configure LLM
export LLM_PROVIDER=openai
export LLM_MODEL=gpt-4o-mini
export OPENAI_API_KEY=sk-...

# 4. Build index (offline)
python -m pipelines.indexing.build_index

# 5. Run CLI
python -m app.cli.main
```

---

## Docker-Based Execution (Canonical)

### Prerequisites

* Docker ≥ 25
* Docker Compose v2
* `.env` file present at project root

Example `.env`:

```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-...
```

---

### 1️⃣ Build Images

```bash
docker build -f docker/Dockerfile.base -t rag-base .
docker compose build
```

* `rag-base` installs all dependencies once
* Other images reuse it

---

### 2️⃣ Build / Update Index (Offline)

```bash
docker compose --profile index run --rm rag-indexer
```

This will:

* read documents from `data/raw/`
* generate embeddings
* write FAISS index to `data/indexes/`

Run this **only when documents change**.

---

### 3️⃣ Run Interfaces

#### CLI

```bash
docker compose run --rm rag-runtime
```

---

#### API

```bash
docker compose up rag-api
```

Then open:

```
http://127.0.0.1:8000/docs
```

---

#### Web UI (Streamlit)

```bash
docker compose up rag-web
```

Then open:

```
http://127.0.0.1:8501
```

---

## Notes on Architecture

* **Docker images never contain data or secrets**
* All persistent state lives in `data/`
* `.env` is injected at runtime via Docker Compose
* Indexing and querying are strictly separated

This mirrors a **production-grade local deployment**.

---

## When to Use Which Mode

| Mode   | Use case                           |
| ------ | ---------------------------------- |
| `uv`   | development, debugging             |
| Docker | reproducibility, demos, deployment |
| CLI    | single-user workflows              |
| API    | programmatic access                |
| Web    | human-facing UI                    |

---

## One-Line Summary

> The system can be run either locally via **uv** or reproducibly via **Docker**, with Docker being the recommended path for deployment-like usage.

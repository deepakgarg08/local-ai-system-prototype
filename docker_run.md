ls data/indexes
**Berlin, Germany — 21 January 2026, 12:13 CET**

TLDR;

# build base
docker build -f docker/Dockerfile.base -t rag-base .

# build all images
docker compose build

# build index
docker compose --profile index run --rm rag-indexer

# run system
docker compose run --rm rag-runtime



**Berlin, Germany — 21 January 2026, 13:26 CET**

Below is a **ready-to-paste `DEPLOYMENT.md`** that exactly matches what you built, tested, and discussed.
This is **clean, reviewer-friendly, and production-aligned**—no aspirational fluff.

---

# DEPLOYMENT.md

## Overview

This document describes **how to deploy and operate** the local-first RAG system using **Docker**.

The deployment model is intentionally simple:

* single machine
* Docker + Docker Compose
* offline indexing
* explicit runtime interfaces (CLI / API / Web)
* no cloud dependency
* no Kubernetes

This is a **software-style deployment**, not a managed SaaS.

---

## Deployment Philosophy

The system follows these principles:

* **Images are immutable**
* **Data is persistent and external**
* **Configuration is injected at runtime**
* **Indexing and querying are strictly separated**
* **Human-in-the-loop is preserved**

Docker is used for **reproducibility and isolation**, not abstraction-heavy orchestration.

---

## Prerequisites

* Linux (tested on Fedora)
* Docker ≥ 25
* Docker Compose v2
* Disk space for models and FAISS index
* Internet access (for model downloads, if applicable)

---

## Repository Layout (Deployment-Relevant)

```
local-ai-system-prototype/
│
├── docker/
│   ├── Dockerfile.base
│   ├── Dockerfile.indexer
│   └── Dockerfile.runtime
│
├── docker-compose.yml
├── .env
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── indexes/
│
├── app/
│   ├── cli/
│   ├── api/
│   └── web/
│
├── pipelines/
├── llms/
└── configs/
```

---

## Configuration (`.env`)

Configuration and secrets are **never baked into images**.

Create a `.env` file at the project root:

```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=sk-...
```

Notes:

* `.env` is injected at runtime via Docker Compose
* `.env` must **not** be committed to Git
* A `.env.example` should be committed instead

---

## Build Phase

### 1️⃣ Build Base Image (Dependencies)

This step installs **all system and Python dependencies once**.

```bash
docker build -f docker/Dockerfile.base -t rag-base .
```

Re-run this **only if `pyproject.toml` changes**.

---

### 2️⃣ Build Runtime Images

```bash
docker compose build
```

This builds:

* `rag-indexer`
* `rag-runtime`

Both reuse `rag-base`.

---

## Indexing Phase (Offline)

Indexing is a **controlled, offline batch operation**.

Run it:

* once initially
* whenever documents in `data/raw/` change

```bash
docker compose --profile index run --rm rag-indexer
```

Outputs:

* FAISS index → `data/indexes/faiss.index`
* metadata → `data/indexes/metadata.json`

The container exits automatically when finished.

---

## Runtime Interfaces

All interfaces use the **same runtime image**, with different entrypoints.

---

### CLI (Default)

Interactive, single-user mode.

```bash
docker compose run --rm rag-runtime
```

Use this for:

* development
* debugging
* local expert usage

---

### API (Service Mode)

Starts the API server (FastAPI).

```bash
docker compose up rag-api
```

Access:

```
http://127.0.0.1:8000/docs
```

This is the **canonical programmatic interface**.

---

### Web UI (Streamlit)

Starts the Streamlit web application.

```bash
docker compose up rag-web
```

Access:

```
http://127.0.0.1:8501
```

Notes:

* Web UI must be started via `streamlit run`
* It is not a generic Python module

---

## Operational Rules (Important)

### Images

* Never modify running containers
* Rebuild images only on code or dependency changes

### Data

* Everything in `data/` is persistent
* Back up `data/` regularly
* Never delete volumes casually

### Configuration

* Change `.env` without rebuilding images
* Restart containers after config changes

### Indexing

* Treat index builds like migrations
* Never rebuild index automatically at runtime

---

## Backup Strategy (Minimal)

At minimum:

```bash
tar czf backup_$(date +%F).tar.gz data/
```

Back up:

* before large refactors
* before index rebuilds
* on a regular schedule

---

## What This Deployment Is NOT

* ❌ Kubernetes-based
* ❌ Auto-scaling
* ❌ Multi-tenant
* ❌ Stateless
* ❌ Cloud-dependent

These are **explicit non-goals** at this stage.

---

## When to Rebuild What

| Change            | Action                 |
| ----------------- | ---------------------- |
| Code change       | `docker compose build` |
| Dependency change | rebuild `rag-base`     |
| Config change     | restart containers     |
| Document change   | rerun indexer          |
| Data loss         | restore from backup    |

---

## Summary

This deployment provides:

* deterministic behavior
* clear operational boundaries
* reproducibility
* local data sovereignty
* multiple user interfaces from one core system

> The system is deployed like serious software — not “AI magic”.

---

If you want, next we can:

* add **production hardening** (healthchecks, limits)
* write an **OPERATIONS.md**
* or document **DevOps vs MLOps vs LLMOps** in project terms

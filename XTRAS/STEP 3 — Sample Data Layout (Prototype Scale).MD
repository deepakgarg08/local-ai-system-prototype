**📅 14 January 2026, 17:44 (Berlin time)**

Great choice. This is the **right next step** — everything in your system will grow outward from data.

We are still **not implementing logic**.
This step defines **what data exists, where it lives, and why**.

---

# STEP 3 — Sample Data Layout (Prototype Scale)

## Goal of this step

Create a **tiny but realistic dataset** that:

* Represents real enterprise data
* Exercises all future pipelines
* Is safe to version-control (or clearly excluded)

Think of this as **training wheels for the full system**.

---

## 1. Design Principles for Sample Data

We follow these rules:

1. **Very small volume**
2. **Multiple document types**
3. **Clear semantic differences**
4. **Human-readable**
5. **Replaceable later with real data**

---

## 2. Target Data Categories (From the Original Project)

We mirror the PDF scope, but shrink it aggressively:

| Category          | Purpose              |
| ----------------- | -------------------- |
| Knowledge docs    | RAG baseline         |
| Functional specs  | Long structured text |
| Contracts         | Clause extraction    |
| Training material | Instructional tone   |

---

## 3. Folder Structure (Concrete)

Inside your project:

```bash
mkdir -p data/raw/{knowledge,contracts,specs,training}
```

Result:

```
data/raw/
├── knowledge/
├── contracts/
├── specs/
└── training/
```

This mirrors **future ETL routing**.

---

## 4. What Goes Into Each Folder (Very Specific)

### 4.1 `knowledge/` — Internal knowledge base

Purpose:

* Policies
* Guidelines
* Reference docs

Examples (you will create tiny ones):

```
company_overview.txt
it_security_policy.txt
```

Each file:

* 1–2 pages max
* Clear headings
* Natural language

---

### 4.2 `contracts/` — Legal-style documents

Purpose:

* Clause extraction
* Metadata detection

Examples:

```
service_agreement.txt
nda_sample.txt
```

Each file:

* Fake parties
* Fake dates
* Realistic structure

⚠️ Never use real contracts.

---

### 4.3 `specs/` — Functional specifications

Purpose:

* Long-document reasoning
* Cross-section queries

Examples:

```
erp_system_spec.txt
user_management_spec.txt
```

Each file:

* Headings
* Sections
* Lists
* “Version” text at top

---

### 4.4 `training/` — Instructional material

Purpose:

* Script generation later
* Training-mode prompts

Examples:

```
onboarding_guide.txt
data_entry_guidelines.txt
```

Tone:

* Instructional
* Step-based

---

## 5. Create Placeholder Files (Now)

Let’s create **one file per category** to start.

```bash
nano data/raw/knowledge/company_overview.txt
```

Add something like:

```text
Company Overview

ACME Systems GmbH is a fictional company used for internal testing.

Mission:
Provide reliable enterprise software solutions.

Departments:
- Engineering
- Sales
- Accounting
```

Repeat similarly for:

* `contracts/service_agreement.txt`
* `specs/erp_system_spec.txt`
* `training/onboarding_guide.txt`

👉 Keep each file **short but structured**.

---

## 6. What We Are NOT Doing Yet

❌ No parsing
❌ No chunking
❌ No embeddings
❌ No indexing

Right now, these files are **just ground truth**.

---

## 7. Git Hygiene Check

Remember: `data/raw/*` is ignored by `.gitignore`.

Confirm:

```bash
git status
```

You should **not** see raw data listed.

This is intentional and correct.

---

## 8. Why This Step Matters

You now have:

* A **realistic data universe**
* Clear semantic separation
* A foundation for:

  * ETL
  * RAG
  * Contract analysis
  * Training modes

This directly mirrors the structure described in the original project document.

---

## Next Step (Recommended)

👉 **Next: Ingestion & Extraction Overview (No Code Yet)**

This will answer:

* How files are discovered
* How types are routed
* Where metadata begins

Reply with:

> **“Next: ingestion & extraction overview”**

We’re building this exactly the right way.

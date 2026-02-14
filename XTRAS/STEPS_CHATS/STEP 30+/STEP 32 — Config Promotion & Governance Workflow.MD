
# 🧱 STEP 32 — Config Promotion & Governance Workflow

## 🎯 Purpose

STEP 32 turns a recommended threshold into an official, versioned runtime configuration.

It closes the loop between:

```
Analysis → Configuration
```

---

## 🧠 Your Config Architecture

Your system loads threshold from:

```
configs/active.yaml
        ↓
configs/versions/<version>.yaml
```

Using:

```python
load_active_config()
```

So promotion must:

* Create a new version file
* Update active.yaml
* Preserve old versions
* Maintain audit history

---

## 🔁 What STEP 32 Does

When you run:

```bash
python tools/promote_threshold.py
```

It:

1️⃣ Reads recommendation file
2️⃣ Reads current active version
3️⃣ Copies that version file
4️⃣ Updates only:

```yaml
retrieval.min_similarity_threshold
```

5️⃣ Updates YAML `version:` field
6️⃣ Creates new version file
7️⃣ Updates `active.yaml`
8️⃣ Appends to:

```
configs/history/threshold_changes.json
```

---

## 📂 Example Lifecycle

Before:

```
active.yaml → v2026_02_08
threshold = 0.30
```

After promotion:

```
active.yaml → v2026_02_15_105812
threshold = 0.34
```

Old version remains untouched.

---

## ⚠ Important Runtime Note

Because `_CONFIG` is cached:

You must restart your application after promotion.

Otherwise old threshold remains in memory.

---

# 🧠 What These Steps Achieve

Together, STEP 31 + STEP 32 create:

* Measured threshold behavior
* Drift detection
* Safe recommendation
* Controlled promotion
* Immutable versioning
* Audit trail
* Reproducible runtime state

---

# 🏗 System Maturity Upgrade

Before:

Threshold = fixed number in YAML.

After:

Threshold = monitored control boundary with governed updates.

---

# 🎯 What They Are NOT

They are not:

* Automatic self-tuning
* Online learning
* Runtime auto-adaptation
* Part of run_rag()

They are offline governance tools.

---

# 🔁 Complete Feedback Loop

```
RAG queries
      ↓
Logs (STEP 30)
      ↓
Drift analysis (STEP 31)
      ↓
Threshold recommendation
      ↓
Manual promotion (STEP 32)
      ↓
New config version
      ↓
Restart system
      ↓
New threshold active
```

This is production-grade configuration governance.

---

If you want next, we can summarize your entire system maturity progression from STEP 14 → STEP 32 in one consolidated architectural view.

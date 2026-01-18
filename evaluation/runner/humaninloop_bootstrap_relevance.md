## `bootstrap_relevance.py`

### Purpose
Automatically generates **candidate relevant chunks** for each golden query by running the retriever and collecting the top-k results.

### Role in the system
- Helps **bootstrap ground truth** for retrieval evaluation  
- Reduces manual effort when creating `relevance_judgments.json`  
- **Does NOT decide correctness** — it only proposes candidates

### How it is used
- Run once (or occasionally) during evaluation setup  
- A human reviews the output and selects the correct `chunk_id` values  
- The reviewed results are then written into `relevance_judgments.json`

### Important rule
This script is a **helper tool only** and is **not part of runtime execution or CI pipelines**.

---

## `relevance_bootstrap.json`

### Purpose
Stores **retrieval candidates** (top-k chunk IDs and text previews) for each golden query.

### What it contains
- Query ID  
- List of retrieved `chunk_id` values  
- Short text previews to assist human review

### What it is NOT
- ❌ Not ground truth  
- ❌ Not frozen  
- ❌ Not used for metrics or regression tests  

### Lifecycle
- Generated automatically by `bootstrap_relevance.py`  
- Manually reviewed by a human  
- Used to create or update `relevance_judgments.json`  
- Can be deleted or regenerated at any time

---

### One-line takeaway
`bootstrap_relevance.py` and `relevance_bootstrap.json` exist to **assist humans in creating correct ground truth**, not to replace human judgment.

These artifacts are part of **STEP 18** and cleanly hand off responsibility to **STEP 19**, where ground truth becomes frozen and enforced.

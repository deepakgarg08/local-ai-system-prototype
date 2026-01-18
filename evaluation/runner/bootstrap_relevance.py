import json
from pipelines.query.retriever import retrieve_context_structured

TOP_K = 5

with open("evaluation/datasets/golden_queries.json") as f:
    queries = json.load(f)

bootstrap = {}

for q in queries:
    retrieved = retrieve_context_structured(q["query"], k=TOP_K)
    bootstrap[q["id"]] = [
        {
            "chunk_id": c["id"],
            "preview": c["text"][:200]
        }
        for c in retrieved
    ]

with open("evaluation/datasets/relevance_bootstrap.json", "w") as f:
    json.dump(bootstrap, f, indent=2)

import json
from pipelines.query.retriever import retrieve_context_structured
from evaluation.metrics.precision import precision_at_k
from evaluation.metrics.recall import recall_at_k
from evaluation.metrics.mrr import reciprocal_rank

def run():
    with open("evaluation/datasets/golden_queries.json") as f:
        queries = json.load(f)

    with open("evaluation/datasets/relevance_judgments.json") as f:
        relevance = json.load(f)

    results = []

    for q in queries:
        retrieved = retrieve_context_structured(q["query"], k=5)

        print("\n==============================")
        print("QUERY ID:", q["id"])
        print("QUERY:", q["query"])
        print("RETRIEVED IDS:")
        retrieved_ids = [c["id"] for c in retrieved]
        for c in retrieved:
            print(" -", c["id"])
        

        rel = relevance.get(q["id"], [])
        print("EXPECTED IDS:", rel)
        print("==============================\n")
      
        results.append({
            "query_id": q["id"],
            "precision@5": precision_at_k(retrieved_ids, rel, 5),
            "recall@5": recall_at_k(retrieved_ids, rel, 5),
            "mrr": reciprocal_rank(retrieved_ids, rel)
        })
        
            # ---------------------------
    # Aggregate Metrics
    # ---------------------------

    total_queries = len(results)

    mean_precision = sum(r["precision@5"] for r in results) / total_queries
    mean_recall = sum(r["recall@5"] for r in results) / total_queries
    mean_mrr = sum(r["mrr"] for r in results) / total_queries

    summary = {
        "mean_precision@5": round(mean_precision, 4),
        "mean_recall@5": round(mean_recall, 4),
        "mean_mrr": round(mean_mrr, 4),
        "num_queries": total_queries
    }

    print("\n===== AGGREGATED METRICS =====")
    for k, v in summary.items():
        print(f"{k}: {v}")
    print("==============================\n")
    
    final_output = {
        "per_query": results,
        "summary": summary
    }

    with open("evaluation/reports/summary_metrics.json", "w") as f:
        json.dump(final_output, f, indent=2)
    
    with open("evaluation/reports/retrieval_metrics_overall.json", "w") as f:
        json.dump(summary, f, indent=2)

if __name__ == "__main__":
    run()

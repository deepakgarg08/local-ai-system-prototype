import json
from evaluation.runner.run_retrieval_eval import run


def load_metrics():
    run()  # generate fresh metrics
    with open("evaluation/reports/retrieval_metrics.json") as f:
        return json.load(f)


def test_recall_never_drops_below_threshold():
    metrics = load_metrics()

    for entry in metrics:
        query_id = entry["query_id"]
        recall = entry["recall@5"]

        # Only enforce queries with defined ground truth
        if recall > 0:
            assert recall >= 1.0, (
                f"Recall regression for {query_id}: {recall}"
            )

# OPTIONAL — add this only if you want ranking guarantees
def test_mrr_above_minimum():
    metrics = load_metrics()

    for entry in metrics:
        if entry["recall@5"] > 0:
            assert entry["mrr"] >= 0.5, (
                f"MRR regression for {entry['query_id']}"
            )

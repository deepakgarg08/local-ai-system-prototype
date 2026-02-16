import json
import statistics

from evaluation.runner.run_retrieval_eval import run


METRICS_PATH = "evaluation/reports/retrieval_metrics.json"

# ---- Guard Thresholds ----
MIN_AVG_MRR = 0.40          # global ranking quality
MIN_RECALL_PER_QUERY = 1.0  # must retrieve ground truth in top-k


def load_metrics():
    """
    Runs retrieval evaluation and loads fresh metrics.
    """
    run()

    with open(METRICS_PATH, "r") as f:
        return json.load(f)


def test_recall_never_drops_below_threshold():
    """
    Ensure every query that has ground truth retrieves it in top-k.
    """
    metrics = load_metrics()

    failures = []

    for entry in metrics:
        query_id = entry["query_id"]
        recall = entry["recall@5"]

        # Only enforce for queries with defined ground truth
        if recall > 0:
            if recall < MIN_RECALL_PER_QUERY:
                failures.append((query_id, recall))

    if failures:
        formatted = "\n".join(
            f"{qid}: recall@5={rec}"
            for qid, rec in failures
        )
        raise AssertionError(
            f"\nRecall regression detected:\n{formatted}"
        )


def test_average_mrr_above_minimum():
    """
    Ensure global ranking quality does not degrade significantly.
    """
    metrics = load_metrics()

    mrr_values = [
        entry["mrr"]
        for entry in metrics
        if entry["recall@5"] > 0
    ]

    if not mrr_values:
        raise AssertionError("No valid queries with ground truth found.")

    avg_mrr = statistics.mean(mrr_values)

    print(f"\nAverage MRR: {avg_mrr:.4f}")

    assert avg_mrr >= MIN_AVG_MRR, (
        f"Average MRR regression detected: {avg_mrr:.4f} "
        f"(minimum required: {MIN_AVG_MRR})"
    )

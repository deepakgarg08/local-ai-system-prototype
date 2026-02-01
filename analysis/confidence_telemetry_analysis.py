import json
from pathlib import Path
from collections import Counter, defaultdict
from statistics import mean


LOG_DIR = Path("logs/confidence")


def load_events():
    events = []
    for file in sorted(LOG_DIR.glob("*.jsonl")):
        for line in file.read_text().splitlines():
            events.append(json.loads(line))
    return events


def main():
    events = load_events()

    if not events:
        print("No telemetry events found.")
        return

    print("=" * 60)
    print("STEP 22 — CONFIDENCE DRIFT ANALYSIS")
    print("=" * 60)

    # --------------------------------------------------
    # 1. Basic counts
    # --------------------------------------------------
    confidence_counts = Counter(e["confidence_level"] for e in events)
    answer_type_counts = Counter(e["answer_type"] for e in events)

    print("\nConfidence distribution:")
    for k, v in confidence_counts.items():
        print(f"  {k}: {v}")

    print("\nAnswer types:")
    for k, v in answer_type_counts.items():
        print(f"  {k}: {v}")

    # --------------------------------------------------
    # 2. Similarity vs confidence
    # --------------------------------------------------
    similarity_by_confidence = defaultdict(list)

    for e in events:
        stats = e.get("retrieval_stats") or {}
        min_sim = stats.get("min_similarity")

        if min_sim is not None:
            similarity_by_confidence[e["confidence_level"]].append(min_sim)

    print("\nAverage MIN similarity by confidence:")
    for level, values in similarity_by_confidence.items():
        print(f"  {level}: {mean(values):.3f}")

    # --------------------------------------------------
    # 3. Risk detection
    # --------------------------------------------------
    risky = [
        e for e in events
        if e["confidence_level"] == "HIGH"
        and e.get("retrieval_stats", {}).get("min_similarity", 1.0) < 0.4
    ]

    print("\nPotential risk cases:")
    print(f"  HIGH confidence with low similarity (<0.4): {len(risky)}")

    if risky:
        print("  Example:")
        example = risky[0]
        print(f"    query: {example['query']}")
        print(f"    min_similarity: {example['retrieval_stats']['min_similarity']}")

    print("\nAnalysis complete.")


if __name__ == "__main__":
    main()

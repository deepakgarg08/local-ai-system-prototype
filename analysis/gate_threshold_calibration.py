# analysis/gate_threshold_calibration.py

"""
STEP 31 — Relevance Gate Stability & Threshold Calibration

This script analyzes decision-level RAG logs and evaluates:

1. Similarity distribution
2. Gate pass/fail separation
3. Threshold stability margin
4. Candidate safer thresholds

This script does NOT modify runtime behavior.
It is purely analytical.
"""

import json
from pathlib import Path
from statistics import mean, median
from collections import defaultdict

# Adjust path if needed
LOG_FILE = Path("logs/rag_events.jsonl")

# Must match your runtime threshold
from configs.loader import load_active_config

config = load_active_config()
MIN_SIMILARITY_THRESHOLD = config["retrieval"]["min_similarity_threshold"]

CURRENT_THRESHOLD = MIN_SIMILARITY_THRESHOLD or 0.31
print(f"Using MIN_SIMILARITY_THRESHOLD analysis/gate_threshold_calibration.py: {CURRENT_THRESHOLD}")


def load_events():
    if not LOG_FILE.exists():
        print("No RAG event log found.")
        return []

    events = []
    with LOG_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            event = json.loads(line)

            # Ignore mock/test models
            backend = event.get("llm", {}).get("backend")
            if backend in {"Mock", "FakeLLM"}:
                continue

            events.append(event)

    return events


def extract_similarity_data(events):
    passed = []
    failed = []

    for e in events:
        sim = e.get("retrieval", {}).get("max_similarity")
        gate = e.get("relevance_gate", {}).get("passed")

        if sim is None:
            continue

        if gate:
            passed.append(sim)
        else:
            failed.append(sim)

    return passed, failed


def print_basic_stats(passed, failed):
    print("=" * 60)
    print("STEP 31 — RELEVANCE GATE CALIBRATION")
    print("=" * 60)

    print(f"\nCurrent threshold: {CURRENT_THRESHOLD:.2f}")
    print(f"Total passed: {len(passed)}")
    print(f"Total failed: {len(failed)}")

    if passed:
        print("\nPASSED SIMILARITIES")
        print(f"  Mean:   {mean(passed):.4f}")
        print(f"  Median: {median(passed):.4f}")
        print(f"  Min:    {min(passed):.4f}")
        print(f"  Max:    {max(passed):.4f}")

    if failed:
        print("\nFAILED SIMILARITIES")
        print(f"  Mean:   {mean(failed):.4f}")
        print(f"  Median: {median(failed):.4f}")
        print(f"  Min:    {min(failed):.4f}")
        print(f"  Max:    {max(failed):.4f}")


def print_distribution(events):
    print("\nSimilarity Distribution (0.1 buckets):")

    buckets = defaultdict(int)

    for e in events:
        sim = e.get("retrieval", {}).get("max_similarity")
        if sim is None:
            continue
        bucket = round(sim, 1)
        buckets[bucket] += 1

    for b in sorted(buckets):
        print(f"  {b:.1f} : {buckets[b]}")


def analyze_stability(events):
    margins = []

    for e in events:
        sim = e.get("retrieval", {}).get("max_similarity")
        if sim is None:
            continue

        margins.append(abs(sim - CURRENT_THRESHOLD))

    if not margins:
        print("\nNot enough data to compute stability margin.")
        return

    avg_margin = mean(margins)

    print("\nThreshold Stability Analysis:")
    print(f"  Average distance from threshold: {avg_margin:.4f}")

    if avg_margin < 0.05:
        print("  ⚠ Threshold sits in high-density similarity region (unstable).")
    else:
        print("  ✓ Threshold appears reasonably separated.")


def suggest_candidate_thresholds(passed, failed):
    print("\nCandidate Threshold Suggestions:")

    if not failed:
        print("  No failed samples — insufficient diversity.")
        return

    max_failed = max(failed)

    # Safe lower bound: above highest failed similarity
    safe_min = round(max_failed + 0.01, 2)

    print(f"  Highest FAILED similarity: {max_failed:.4f}")
    print(f"  Safe minimum threshold: {safe_min:.2f}")

    # Conservative threshold: 25th percentile of passed
    if len(passed) >= 4:
        sorted_passed = sorted(passed)
        idx = int(0.25 * len(sorted_passed))
        conservative = round(sorted_passed[idx], 2)

        print(f"  Conservative threshold (25th percentile PASSED): {conservative:.2f}")

        print("\nRecommended operating range:")
        print(f"    {safe_min:.2f}  →  {conservative:.2f}")
    else:
        print("  Not enough PASSED samples for percentile analysis.")


def main():
    events = load_events()

    if not events:
        print("No valid events found.")
        return

    passed, failed = extract_similarity_data(events)

    print_basic_stats(passed, failed)
    print_distribution(events)
    analyze_stability(events)
    suggest_candidate_thresholds(passed, failed)

    print("\nCalibration complete.")


if __name__ == "__main__":
    main()

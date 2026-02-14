# analysis/gate_drift_monitor.py

import json
from pathlib import Path
from statistics import mean
from datetime import datetime

LOG_FILE = Path("logs/rag_events.jsonl")

RECENT_SAMPLE_SIZE = 50
CURRENT_THRESHOLD = 0.30
SAFETY_MARGIN = 0.02


def load_events():
    if not LOG_FILE.exists():
        return []

    events = []
    with LOG_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            e = json.loads(line)
            if e.get("llm", {}).get("backend") in {"Mock", "FakeLLM"}:
                continue
            events.append(e)

    return events


def parse_timestamp(ts):
    return datetime.fromisoformat(ts)


def extract_similarity(sample):
    return [
        e["retrieval"]["max_similarity"]
        for e in sample
        if e["retrieval"]["max_similarity"] is not None
    ]


def extract_pass_rate(sample):
    passes = [e["relevance_gate"]["passed"] for e in sample]
    return sum(passes) / len(passes) if passes else 0


def recommend_threshold(sample):
    failed_sims = [
        e["retrieval"]["max_similarity"]
        for e in sample
        if not e["relevance_gate"]["passed"]
        and e["retrieval"]["max_similarity"] is not None
    ]

    if not failed_sims:
        return None

    highest_failed = max(failed_sims)
    return round(highest_failed + SAFETY_MARGIN, 2)


def monitor_drift(events):
    if len(events) < RECENT_SAMPLE_SIZE * 2:
        print("Not enough data for drift analysis.")
        return

    events.sort(key=lambda e: parse_timestamp(e["timestamp"]))

    historical = events[:-RECENT_SAMPLE_SIZE]
    recent = events[-RECENT_SAMPLE_SIZE:]

    hist_mean = mean(extract_similarity(historical))
    recent_mean = mean(extract_similarity(recent))

    hist_pass = extract_pass_rate(historical)
    recent_pass = extract_pass_rate(recent)

    sim_delta = recent_mean - hist_mean
    pass_delta = recent_pass - hist_pass

    print("=" * 60)
    print("STEP 31 — DRIFT MONITOR WITH THRESHOLD RECOMMENDATION")
    print("=" * 60)

    print("\nCurrent threshold:", CURRENT_THRESHOLD)

    print("\nSimilarity Mean:")
    print(f"  Historical: {hist_mean:.4f}")
    print(f"  Recent:     {recent_mean:.4f}")
    print(f"  Delta:      {sim_delta:.4f}")

    print("\nPass Rate:")
    print(f"  Historical: {hist_pass:.2%}")
    print(f"  Recent:     {recent_pass:.2%}")
    print(f"  Delta:      {pass_delta:.2%}")

    drift_detected = False

    if abs(sim_delta) > 0.05:
        print("\n⚠ Significant similarity drift detected.")
        drift_detected = True

    if abs(pass_delta) > 0.10:
        print("\n⚠ Significant pass-rate drift detected.")
        drift_detected = True

    if drift_detected:
        new_threshold = recommend_threshold(recent)

        print("\n--- Automatic Threshold Recommendation ---")

        if new_threshold is None:
            print("Not enough failed cases to compute recommendation.")
        else:
            print(f"Suggested new threshold: {new_threshold:.2f}")

            if new_threshold > CURRENT_THRESHOLD:
                print("Recommendation: Increase threshold for safety.")
            elif new_threshold < CURRENT_THRESHOLD:
                print("Recommendation: Lower threshold to improve recall.")
            else:
                print("Threshold appears optimal.")

    else:
        print("\n✓ No significant drift detected. Threshold stable.")

    print("\nDrift monitoring complete.")


if __name__ == "__main__":
    events = load_events()
    monitor_drift(events)

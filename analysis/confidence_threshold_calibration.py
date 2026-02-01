import json
from pathlib import Path
from statistics import mean
from collections import defaultdict


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

    # --------------------------------------------------
    # Separate answer types
    # --------------------------------------------------
    answered = []
    idk = []

    for e in events:
        sim = e.get("retrieval_stats", {}).get("min_similarity")
        if sim is None:
            continue

        if e["answer_type"] == "ANSWER":
            answered.append(sim)
        else:
            idk.append(sim)

    print("=" * 60)
    print("STEP 23 — THRESHOLD CALIBRATION")
    print("=" * 60)

    print(f"\nTotal events: {len(events)}")
    print(f"Answered: {len(answered)}")
    print(f"IDK: {len(idk)}")

    if not answered or not idk:
        print("\nNot enough diversity to calibrate thresholds.")
        return

    # --------------------------------------------------
    # Basic statistics
    # --------------------------------------------------
    print("\nSimilarity statistics:")
    print(f"  ANSWER  avg min_similarity: {mean(answered):.3f}")
    print(f"  IDK     avg min_similarity: {mean(idk):.3f}")

    # --------------------------------------------------
    # Candidate threshold search
    # --------------------------------------------------
    candidates = [round(x, 2) for x in [i / 100 for i in range(20, 90, 5)]]

    print("\nCandidate thresholds:")
    for t in candidates:
        false_answers = sum(1 for s in answered if s < t)
        false_idks = sum(1 for s in idk if s >= t)

        print(
            f"  t={t:.2f} | "
            f"ANSWER below t: {false_answers:3d} | "
            f"IDK above t: {false_idks:3d}"
        )

    # --------------------------------------------------
    # Recommendation heuristic
    # --------------------------------------------------
    safe_thresholds = [
        t for t in candidates
        if sum(1 for s in answered if s < t) <= max(1, len(answered) * 0.05)
    ]

    print("\nRecommended threshold(s):", safe_thresholds)
    if safe_thresholds:
        for t in safe_thresholds[:3]:
            print(f"  ≥ {t:.2f}")
    else:
        print("  No safe threshold found — corpus quality may be insufficient.")

    print("\nCalibration complete.")


if __name__ == "__main__":
    main()

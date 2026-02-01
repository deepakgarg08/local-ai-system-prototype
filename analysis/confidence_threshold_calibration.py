import json
from pathlib import Path
from statistics import mean
from collections import defaultdict


LOG_DIR = Path("logs/confidence/runtime")


def load_events():
    events = []
    for file in sorted(LOG_DIR.glob("*.jsonl")):
        for line in file.read_text().splitlines():
            e = json.loads(line)

            # ⛔ HARD GUARD: ignore test / mock telemetry
            if e.get("model_backend") in {"Mock", "FakeLLM"}:
                continue

            events.append(e)
    return events


def main():
    events = load_events()

    if not events:
        print("No telemetry events found.")
        return

    result = analyze_thresholds(events)

    print("=" * 60)
    print("STEP 23 — THRESHOLD CALIBRATION")
    print("=" * 60)

    print(f"\nTotal events: {result['total_events']}")
    print(f"Answered: {result['answered']}")
    print(f"IDK: {result['idk']}")

    if not result["similarity_stats"]:
        print("\nNot enough diversity to calibrate thresholds.")
        return

    print("\nSimilarity statistics:")
    print(
        f"  ANSWER  avg min_similarity: "
        f"{result['similarity_stats']['answer_avg']:.3f}"
    )
    print(
        f"  IDK     avg min_similarity: "
        f"{result['similarity_stats']['idk_avg']:.3f}"
    )

    print("\nCandidate thresholds:")
    for t in result["candidate_thresholds"]:
        false_answers = sum(
            1 for e in events
            if e.get("answer_type") == "ANSWER"
            and e.get("retrieval_stats", {}).get("min_similarity", 0) < t
        )
        false_idks = sum(
            1 for e in events
            if e.get("answer_type") != "ANSWER"
            and e.get("retrieval_stats", {}).get("min_similarity", 0) >= t
        )

        print(
            f"  t={t:.2f} | "
            f"ANSWER below t: {false_answers:3d} | "
            f"IDK above t: {false_idks:3d}"
        )

    print("\nRecommended threshold(s):", result["recommended_thresholds"])
    if not result["recommended_thresholds"]:
        print("  No safe threshold found — corpus quality may be insufficient.")

    print("\nCalibration complete.")


def analyze_thresholds(events: list[dict]) -> dict:
    answered = []
    idk = []

    for e in events:
        sim = e.get("retrieval_stats", {}).get("min_similarity")
        if sim is None:
            continue

        if e.get("answer_type") == "ANSWER":
            answered.append(sim)
        else:
            idk.append(sim)

    result = {
        "total_events": len(events),
        "answered": len(answered),
        "idk": len(idk),
        "similarity_stats": {},
        "candidate_thresholds": [],
        "recommended_thresholds": [],
    }

    if not answered or not idk:
        return result

    result["similarity_stats"] = {
        "answer_avg": mean(answered),
        "idk_avg": mean(idk),
    }

    candidates = [round(i / 100, 2) for i in range(20, 90, 5)]
    result["candidate_thresholds"] = candidates

    safe_thresholds = [
        t for t in candidates
        if sum(1 for s in answered if s < t) <= max(1, len(answered) * 0.05)
    ]

    result["recommended_thresholds"] = safe_thresholds
    return result


if __name__ == "__main__":

    main()

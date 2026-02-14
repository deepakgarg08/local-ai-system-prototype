import subprocess
import sys
import time
import json
from pathlib import Path
from typing import List, Dict


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)


# --------------------------------------------------
# TASK REGISTRY
# --------------------------------------------------

TASKS: List[Dict] = [
    {"module": "pipelines.ingestion.ingest_txt", "category": "pipeline", "requires_llm": False},
    {"module": "pipelines.chunking.chunk_sections", "category": "pipeline", "requires_llm": False},
    {"module": "pipelines.indexing.build_index", "category": "pipeline", "requires_llm": False},
    {"module": "evaluation.runner.run_retrieval_eval", "category": "evaluation", "requires_llm": False},
    {"module": "analysis.gate_threshold_calibration", "category": "analysis", "requires_llm": False},
    {"module": "analysis.gate_drift_monitor", "category": "analysis", "requires_llm": False},

    {"module": "llms.check_llm_working", "category": "infrastructure_validation", "requires_llm": True},
    {"module": "tools.check_llm_health", "category": "admin", "requires_llm": True},
    {"module": "tools.run_confidence_calibration", "category": "admin", "requires_llm": True},
    {"module": "analysis.confidence_threshold_calibration", "category": "analysis", "requires_llm": True},
    {"module": "analysis.confidence_telemetry_analysis", "category": "analysis", "requires_llm": True},
]


# --------------------------------------------------
# EXECUTION
# --------------------------------------------------

def run_module(module_name: str) -> Dict:
    print(f"\n▶ Running module: {module_name}")
    print("-" * 60)

    start = time.time()

    result = subprocess.run(
        [sys.executable, "-m", module_name],
        cwd=PROJECT_ROOT
    )

    duration = round(time.time() - start, 2)

    success = result.returncode == 0

    status = "SUCCESS" if success else "FAILED"

    print(f"{status} | {module_name} | {duration}s")

    return {
        "module": module_name,
        "status": status,
        "duration_seconds": duration,
        "return_code": result.returncode
    }


def run_all(category_filter=None):
    results = []

    non_llm = []
    llm = []

    for task in TASKS:
        if category_filter and task["category"] != category_filter:
            continue

        if task["requires_llm"]:
            llm.append(task)
        else:
            non_llm.append(task)

    print("\n==============================")
    print(" Running NON-LLM tasks first ")
    print("==============================")

    for task in non_llm:
        results.append(run_module(task["module"]))

    print("\n==============================")
    print(" Running LLM-dependent tasks ")
    print("==============================")

    for task in llm:
        results.append(run_module(task["module"]))

    return results


# --------------------------------------------------
# REPORTING
# --------------------------------------------------

def print_summary(results: List[Dict]):
    print("\n\n==============================")
    print(" EXECUTION SUMMARY ")
    print("==============================")

    success_count = 0
    fail_count = 0
    total_time = 0

    for r in results:
        total_time += r["duration_seconds"]
        if r["status"] == "SUCCESS":
            success_count += 1
        else:
            fail_count += 1

        print(f"{r['status']:8} | {r['duration_seconds']:6}s | {r['module']}")

    print("\n--------------------------------")
    print(f"Total tasks: {len(results)}")
    print(f"Success: {success_count}")
    print(f"Failed: {fail_count}")
    print(f"Total time: {round(total_time,2)}s")
    print("--------------------------------\n")


def write_json_report(results: List[Dict]):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    report_path = REPORT_DIR / f"execution_report_{timestamp}.json"

    summary = {
        "timestamp": timestamp,
        "total_tasks": len(results),
        "success": sum(1 for r in results if r["status"] == "SUCCESS"),
        "failed": sum(1 for r in results if r["status"] == "FAILED"),
        "total_runtime_seconds": round(sum(r["duration_seconds"] for r in results), 2),
        "tasks": results
    }

    with open(report_path, "w") as f:
        json.dump(summary, f, indent=4)

    print(f"\nJSON report written to:")
    print(report_path.resolve())


# --------------------------------------------------
# CLI
# --------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--category", type=str, help="Filter by category")
    args = parser.parse_args()

    results = run_all(category_filter=args.category)

    print_summary(results)
    write_json_report(results)

import json
from pathlib import Path

PROJECT_ROOT = Path(".")
OUTPUT_FILE = Path("analysis/manual_entrypoints_report.json")

EXCLUDE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    ".idea",
    ".mypy_cache",
}


def is_excluded(path: Path) -> bool:
    return any(part in EXCLUDE_DIRS for part in path.parts)


def contains_main_block(file_path: Path) -> bool:
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return False
    return 'if __name__ == "__main__"' in content


def classify_file(path: Path) -> str:
    if "analysis" in path.parts:
        return "analysis"
    if "tools" in path.parts:
        return "admin"
    if "evaluation" in path.parts:
        return "evaluation"
    if "pipelines" in path.parts:
        return "pipeline"
    if "scripts" in path.parts:
        return "runtime_script"
    if "app" in path.parts:
        return "runtime_entry"
    if "XTRAS" in path.parts:
        return "archived"
    return "other"


def main():
    python_files = list(PROJECT_ROOT.rglob("*.py"))
    results = []

    for file in python_files:
        if is_excluded(file):
            continue

        if contains_main_block(file):
            results.append({
                "path": str(file),
                "category": classify_file(file),
            })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    print(f"Saved report to: {OUTPUT_FILE}")
    print(f"Total entrypoints: {len(results)}")


if __name__ == "__main__":
    main()

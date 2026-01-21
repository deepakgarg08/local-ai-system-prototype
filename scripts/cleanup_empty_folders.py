#!/usr/bin/env python3

from pathlib import Path

# 🔒 RESTRICT SCOPE HERE
PROJECT_ROOT = Path("docs").resolve()

ALLOWED_EMPTY_FILES = {"__init__.py"}

def is_blank_file(path: Path) -> bool:
    try:
        return path.is_file() and path.read_text(encoding="utf-8").strip() == ""
    except Exception:
        return False


def is_deletable_dir(path: Path) -> bool:
    if not path.is_dir():
        return False

    for item in path.iterdir():
        if item.is_dir():
            if not is_deletable_dir(item):
                return False
        else:
            if item.name in ALLOWED_EMPTY_FILES:
                if not is_blank_file(item):
                    return False
            elif item.suffix == ".md":
                if not is_blank_file(item):
                    return False
            else:
                return False

    return True


def delete_deletable_dirs(root: Path):
    for path in sorted(root.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if is_deletable_dir(path):
            # print(f"[DRY-RUN] Would delete: {path}")
            print(f"Deleting directory: {path}")
            path.rmdir()



if __name__ == "__main__":
    delete_deletable_dirs(PROJECT_ROOT)

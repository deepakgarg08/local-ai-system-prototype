#!/usr/bin/env python3

import os
from pathlib import Path


# Hard-coded extra exclusions
EXTRA_EXCLUDES = {
    "XTRAS",
    ".git",
    ".pytest_cache",
}


def load_gitignore_patterns(root: Path):
    """
    Reads .gitignore and returns cleaned patterns.
    Supports simple wildcard matching via Path.match.
    """
    gitignore = root / ".gitignore"
    patterns = []

    if gitignore.exists():
        with open(gitignore, "r") as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue
                if line.startswith("#"):
                    continue

                patterns.append(line)

    return patterns


def is_ignored(path: Path, root: Path, patterns):
    """
    Checks whether path should be excluded.
    """

    # 1️⃣ Hard exclusions
    if path.name in EXTRA_EXCLUDES:
        return True

    # 2️⃣ .gitignore patterns
    try:
        relative_path = path.relative_to(root)
    except ValueError:
        return False

    for pattern in patterns:
        # Handle directory patterns like "build/"
        if pattern.endswith("/"):
            if relative_path.match(pattern.rstrip("/")):
                return True
            if relative_path.match(pattern):
                return True

        # Handle wildcard patterns (*.pyc etc.)
        if relative_path.match(pattern):
            return True

    return False


def build_tree(root: Path, current: Path, prefix: str, output: list, patterns):
    entries = sorted(
        [
            e for e in current.iterdir()
            if not is_ignored(e, root, patterns)
        ],
        key=lambda x: (x.is_file(), x.name.lower())
    )

    total = len(entries)

    for index, entry in enumerate(entries):
        connector = "└── " if index == total - 1 else "├── "
        output.append(f"{prefix}{connector}{entry.name}")

        if entry.is_dir():
            extension = "    " if index == total - 1 else "│   "
            build_tree(root, entry, prefix + extension, output, patterns)


def main():
    project_root = Path(".").resolve()

    patterns = load_gitignore_patterns(project_root)

    output = []
    output.append(f"{project_root.name}/")

    build_tree(project_root, project_root, "", output, patterns)

    tree_output = "\n".join(output)

    print(tree_output)

    # Save to file
    with open("project_structure.txt", "w") as f:
        f.write(tree_output)


if __name__ == "__main__":
    main()

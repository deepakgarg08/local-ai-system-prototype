import json
import yaml
from pathlib import Path
from datetime import datetime, timezone
RECOMMENDATION_FILE = Path(
    "analysis/recommendations/threshold_recommendation.json"
)

ACTIVE_FILE = Path("configs/active.yaml")
VERSIONS_DIR = Path("configs/versions")
HISTORY_FILE = Path("configs/history/threshold_changes.json")


def load_recommendation():
    if not RECOMMENDATION_FILE.exists():
        raise FileNotFoundError("No threshold recommendation found.")

    with RECOMMENDATION_FILE.open("r") as f:
        return json.load(f)


def load_active_version():
    with ACTIVE_FILE.open("r") as f:
        active = yaml.safe_load(f)
    return active["version"]


def generate_new_version_name():
    return datetime.now(timezone.utc).strftime("v%Y_%m_%d_%H%M%S")


def promote():
    recommendation = load_recommendation()
    current_version = load_active_version()

    current_path = VERSIONS_DIR / f"{current_version}.yaml"

    if not current_path.exists():
        raise FileNotFoundError(f"Active version file not found: {current_path}")

    with current_path.open("r") as f:
        config = yaml.safe_load(f)

    old_threshold = config["retrieval"]["min_similarity_threshold"]
    new_threshold = recommendation["recommended_threshold"]

    if old_threshold == new_threshold:
        print("Threshold unchanged. Promotion skipped.")
        return

    # Create new version name
    new_version = generate_new_version_name()
    new_version_path = VERSIONS_DIR / f"{new_version}.yaml"

    if new_version_path.exists():
        raise RuntimeError(
            f"Version file already exists: {new_version_path}"
        )

    # Update threshold
    config["retrieval"]["min_similarity_threshold"] = new_threshold

    # Update version field inside YAML
    config["version"] = new_version

    # Write new version file
    with new_version_path.open("w") as f:
        yaml.safe_dump(config, f, sort_keys=False)

    print(f"New config version created: {new_version}.yaml")

    # Update active.yaml
    with ACTIVE_FILE.open("w") as f:
        yaml.safe_dump({"version": new_version}, f)

    print(f"Active config updated → {new_version}")

    update_history(
        from_version=current_version,
        to_version=new_version,
        old_threshold=old_threshold,
        new_threshold=new_threshold,
    )


def update_history(from_version, to_version, old_threshold, new_threshold):
    if HISTORY_FILE.exists():
        with HISTORY_FILE.open("r") as f:
            history = json.load(f)
    else:
        history = []

    history.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "from_version": from_version,
        "to_version": to_version,
        "old_threshold": old_threshold,
        "new_threshold": new_threshold,
    })

    with HISTORY_FILE.open("w") as f:
        json.dump(history, f, indent=2)

    print("Promotion history updated.")


if __name__ == "__main__":
    promote()

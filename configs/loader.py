import yaml
from pathlib import Path

_CONFIG = None

def load_active_config():
    global _CONFIG
    if _CONFIG is None:
        with open(Path("configs/active.yaml")) as f:
            active = yaml.safe_load(f)

        version = active["version"]
        with open(Path(f"configs/versions/{version}.yaml")) as f:
            _CONFIG = yaml.safe_load(f)
    print(f"Loaded _CONFIG : {_CONFIG}")
    return _CONFIG

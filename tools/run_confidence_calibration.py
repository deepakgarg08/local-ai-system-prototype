"""
Runs the full confidence calibration workflow.
It mimics the MakeFile, either run MakeFile or this script.

Covers:
- STEP 21 — Telemetry generation
- STEP 22 — Telemetry analysis
- STEP 23 — Threshold calibration
"""

import subprocess
# from dotenv import load_dotenv
# load_dotenv()
from dotenv import dotenv_values
env_dict = dotenv_values(".env")

print("...............",env_dict)

def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    run(["python", "evaluation/run_confidence_calibration_set.py"])
    run(["python", "analysis/confidence_telemetry_analysis.py"])
    run(["python", "analysis/confidence_threshold_calibration.py"])


if __name__ == "__main__":
    main()

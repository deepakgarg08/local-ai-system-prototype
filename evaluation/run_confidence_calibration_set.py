from pipelines.query.run_rag import run_rag
from dotenv import load_dotenv
load_dotenv()
from dotenv import dotenv_values
env_dict = dotenv_values(".env")

print("...........s....",env_dict)
"""
    Confidence calibration question runner.

    Triggers telemetry required for:
    - STEP 21 — Confidence Telemetry & Logging
    - STEP 22 — Confidence Telemetry Analysis
    - STEP 23 — Threshold Calibration
"""
CALIBRATION_QUESTIONS = [

    # --- Category A: High-confidence in-scope ---
    "What is the contract duration of the service agreement?",
    "What is the termination notice period defined in the service agreement?",
    "Which law governs the service agreement?",
    "Who are the parties involved in the service agreement?",
    "What is the mission of ACME Systems GmbH?",
    "What are the core values of ACME Systems GmbH?",
    "Which departments exist at ACME Systems GmbH?",

    # --- Category B: Section-specific ---
    "What are the key rules defined in the IT Security Policy?",
    "Who holds final responsibility according to the IT Security Policy?",
    "What user management features are described in the ERP functional specification?",
    "What functions are included in the accounting module of the ERP system?",
    "What reporting capabilities does the ERP system provide?",

    # --- Category C: Cross-document reasoning ---
    "Which document explains access rights and role assignment at ACME Systems GmbH?",
    "What steps must a new employee complete to comply with security requirements?",
    "Which documents mention responsibilities related to security or compliance?",

    # --- Category D: Out-of-scope ---
    "What penalties apply if the client breaches the service agreement?",
    "What encryption algorithms are required by the IT security policy?",
    "Does the ERP system support multi-currency accounting?",
    "Who is the CEO of ACME Systems GmbH?",
    "What happens after the contract duration ends?",
]


def main():
    print("=" * 60)
    print("STEP 23 — RUNNING CALIBRATION QUESTION SET")
    print("=" * 60)

    for i, question in enumerate(CALIBRATION_QUESTIONS, start=1):
        print(f"\n[{i:02d}] {question}")
        result = run_rag(question)

        try:
            result = run_rag(question)
        except Exception as e:
            print(f"→ ERROR: {e}")
            continue

        if result is None:
            print("→ ERROR: run_rag returned None")
            continue

        if result.answer is None:
            print("→ IDK")
        else:
            print("→ ANSWER")
            print(result.answer[:200])


            print("\nAll calibration questions executed.")
            print("Telemetry written to logs/confidence/.")


if __name__ == "__main__":
    main()

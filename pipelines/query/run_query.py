# scripts/run_query.py

"""
CLI entry point for the local RAG system.
This is a thin wrapper around pipelines.query.run_rag.
"""

from pipelines.query.run_rag import run_rag


def main() -> None:
    print("Local AI Query System (type 'exit' to quit)")

    while True:
        query = input("\n> ").strip()
        if query.lower() in {"exit", "quit"}:
            break

        try:
            result = run_rag(query)

            print("\n--- ANSWER ---\n")

            if result.answer is None:
                print(
                    "I don't know. "
                    "The available documents do not contain "
                    "relevant information to answer this question."
                )
            else:
                print(result.answer)

            print("\n--- CONFIDENCE ---")
            print(result.confidence.confidence_level.upper())
            for reason in result.confidence.rationale:
                print(f"- {reason}")

        except Exception as e:
            print(f"\n[ERROR] {e}")


if __name__ == "__main__":
    main()

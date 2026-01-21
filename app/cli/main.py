
import os
from dotenv import load_dotenv
load_dotenv()  # loads .env into os.environ

print(os.getenv("LLM_PROVIDER"))
print(os.getenv("LLM_MODEL"))

from pipelines.query.run_rag import run_rag


BANNER = """
=====================================
 Local AI Assistant
=====================================
Type your question and press Enter.
Type 'exit' or 'quit' to leave.
-------------------------------------
"""


def main():
    print(BANNER)

    while True:
        try:
            query = input(">> ").strip()

            if not query:
                continue

            if query.lower() in {"exit", "quit"}:
                print("\nSession ended.")
                break

            answer = run_rag(
                query=query,
                top_k=5,   # keep fixed & explicit
            )

            if answer.answer:
                print(answer.answer)
            else:
                print("No sufficiently grounded answer found.")

            print("\n-------------------------------------\n")

        except KeyboardInterrupt:
            print("\n\nInterrupted. Exiting cleanly.")
            break


if __name__ == "__main__":
    main()

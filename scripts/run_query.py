# scripts/run_query.py

"""
CLI entry point for the local RAG system.

Responsibilities:
- Call run_rag (single orchestration authority)
- Convert RAGResult into human-readable output
- Display confidence and rationale
"""

import os
from dotenv import load_dotenv
load_dotenv()  # loads .env into os.environ

print(os.getenv("LLM_PROVIDER"))

from pipelines.query.run_rag import run_rag

def main() -> None:
    query = "Who won the FIFA world cup in 2014?"
    query = "what is the termination condition from the company"
    query = "Explain the theory of relativity in simple terms."
    query = "Why not to join acm company?"
    query = "what are company policies"
    # query = input("Enter your question: ")

    result = run_rag(query, top_k=4)

    print("\n==============================")
    print("QUERY")
    print("==============================")
    print(query)

    print("\n==============================")
    print("ANSWER")
    print("==============================")

    if result.answer is None:
        print(
            "I don't know.\n"
            "The available documents do not contain "
            "relevant information to answer this question."
        )
    else:
        print(result.answer)

    print("\n==============================")
    print("CONFIDENCE")
    print("==============================")
    print(result.confidence.confidence_level.upper())

    if result.confidence.rationale:
        print("\nRationale:")
        for reason in result.confidence.rationale:
            print(f"- {reason}")

    print("\n==============================")
    print("SOURCES (retrieval only)")
    print("==============================")
    if not result.sources:
        print("No sources used.")
    else:
        for i, src in enumerate(result.sources, 1):
            print(
                f"[{i}] "
                f"score={src.similarity_score:.3f} | "
                f"document={src.source_document} | "
                f"text={src.chunk_text[:120]}..."
            )


if __name__ == "__main__":
    main()

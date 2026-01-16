"""
End-to-end query pipeline:
User query → retrieval → prompt → Ollama → answer
"""

from pipelines.query.retriever import retrieve_context
from pipelines.query.prompt_builder import build_prompt
from pipelines.query.llm_ollama import run_ollama


def answer_query(query: str) -> str:
    contexts = retrieve_context(query)

    print("\n[RETRIEVED CHUNKS]")
    for i, c in enumerate(contexts, 1):
        print(f"\n--- Chunk {i} ---\n{c[:500]}")

    prompt = build_prompt(query, contexts)
    return run_ollama(prompt)


if __name__ == "__main__":
    print("Local AI Query System (type 'exit' to quit)")

    while True:
        query = input("\n> ")
        if query.lower() in {"exit", "quit"}:
            break

        try:
            answer = answer_query(query)
            print("\n--- ANSWER ---\n")
            print(answer)
        except Exception as e:
            print(f"\n[ERROR] {e}")

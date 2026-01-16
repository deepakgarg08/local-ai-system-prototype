from pipelines.retrieval.scoring import apply_retrieval_strategy
from pipelines.prompting.prompt_builder import build_prompt


def fake_vector_search(query: str):
    """
    TEMPORARY stub.
    Simulates vector DB output.
    """
    return [
        {
            "text": "Vector databases store embeddings for similarity search.",
            "source": "rag_intro.pdf",
            "section": "1.1",
            "page": 2,
            "score": 0.92,
        },
        {
            "text": "Chunking improves retrieval accuracy by preserving semantics.",
            "source": "rag_intro.pdf",
            "section": "2.3",
            "page": 7,
            "score": 0.61,
        },
        {
            "text": "LLMs generate text probabilistically.",
            "source": "llm_basics.pdf",
            "section": "1.0",
            "page": 1,
            "score": 0.18,
        },
    ]


def main():
    query = "What is a vector database?"

    # STEP 7a — retrieval strategy
    raw_chunks = fake_vector_search(query)
    final_chunks = apply_retrieval_strategy(
        raw_chunks,
        top_k=5,
        score_threshold=0.25,
    )

    # STEP 7b — prompt assembly
    prompt, citations = build_prompt(
        query=query,
        chunks=final_chunks,
    )

    print("\n===== FINAL PROMPT =====\n")
    print(prompt)
    print("\n===== CITATIONS MAP =====\n")
    for k, v in citations.items():
        print(f"[{k}] -> {v['source']} page {v['page']}")


if __name__ == "__main__":
    main()

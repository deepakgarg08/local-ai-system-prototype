from typing import List, Dict, Tuple

def build_prompt(
    query: str,
    chunks: List[Dict],
    max_context_tokens: int = 3000,
    buffer_tokens: int = 800,
) -> Tuple[str, Dict[int, Dict]]:
    """
    Build a citation-aware prompt from retrieved chunks.

    Returns:
        prompt (str)
        citations (dict[int, chunk_metadata])
    """

    budget = max_context_tokens - buffer_tokens
    used_tokens = 0

    context_blocks = []
    citations = {}

    for i, ch in enumerate(chunks, start=1):
        text = ch["text"]
        token_estimate = len(text.split())  # replace later with tokenizer

        if used_tokens + token_estimate > budget:
            break

        block = (
            f"[{i}] (source: {ch['source']}, "
            f"section: {ch['section']}, page: {ch['page']})\n"
            f"{text}"
        )

        context_blocks.append(block)
        citations[i] = ch
        used_tokens += token_estimate

    context_text = "\n\n".join(context_blocks)

    prompt = f"""
You are a precise technical assistant.
Answer ONLY using the provided context.
If the answer is not in the context, say so.
Cite facts using [n].

### Context
{context_text}

### Question
{query}

### Answer
""".strip()

    return prompt, citations

# Example usage, can be removed in production
if __name__ == "__main__":
    dummy_chunks = [
        {
            "text": "Vector databases store embeddings for similarity search.",
            "source": "rag_intro.pdf",
            "section": "1.1",
            "page": 2,
            "score": 0.9,
        }
    ]

    prompt, citations = build_prompt(
        query="What is a vector database?",
        chunks=dummy_chunks,
    )

    print(prompt)
    print("\nCITATIONS:", citations)

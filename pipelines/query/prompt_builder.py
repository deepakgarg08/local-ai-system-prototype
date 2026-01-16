"""
Prompt construction logic
"""


def build_prompt(query: str, contexts: list[str]) -> str:
    """
    Assemble the final prompt sent to the LLM.
    """
    context_block = "\n\n---\n\n".join(contexts)

    prompt = f"""
You are a helpful assistant.
Answer the question strictly using the provided context.
If the answer is not contained in the context, say you don't know.

Context:
{context_block}

Question:
{query}

Answer:
""".strip()

    return prompt

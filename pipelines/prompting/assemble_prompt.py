# pipelines/prompting/assemble_prompt.py

from typing import List, Dict, Optional


DEFAULT_SYSTEM_INSTRUCTION = (
    "You are a precise technical assistant. "
    "Answer only using the provided context. "
    "Do not use outside knowledge."
)


def assemble_prompt(
    query: str,
    context_chunks: List[Dict],
    system_instruction: Optional[str] = None,
) -> str:
    """
    Assemble the final prompt string for an LLM.

    Parameters
    ----------
    query : str
        User question
    context_chunks : List[Dict]
        Retrieved chunks from vector search.
        Each dict must contain at least a 'text' field.
    system_instruction : Optional[str]
        Optional system-level instruction.

    Returns
    -------
    str
        Fully assembled prompt
    """

    system_instruction = system_instruction or DEFAULT_SYSTEM_INSTRUCTION

    if not context_chunks:
        context_block = "No relevant context was retrieved."
    else:
        context_block_lines = []
        for idx, chunk in enumerate(context_chunks, start=1):
            text = chunk.get("text", "").strip()
            source = chunk.get("source", "unknown")
            chunk_id = chunk.get("chunk_id", "n/a")

            context_block_lines.append(
                f"[{idx}] (source: {source}, chunk: {chunk_id})\n{text}"
            )

        context_block = "\n\n".join(context_block_lines)

    prompt = f"""
SYSTEM:
{system_instruction}

CONTEXT:
{context_block}

QUESTION:
{query}

INSTRUCTIONS:
- Answer only using the CONTEXT above
- If the answer is not present, say "I don't know"
- Be concise and precise
""".strip()

    return prompt

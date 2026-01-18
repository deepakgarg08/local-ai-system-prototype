# pipelines/prompting/assemble_prompt.py

from typing import List, Dict, Optional


DEFAULT_SYSTEM_INSTRUCTION = (
    "You are a precise technical assistant. "
    "Answer only using the provided context. "
    "Do not use outside knowledge."
)

BASE_INSTRUCTION = """
You MUST answer only using the provided context.
You MUST NOT use any external knowledge.
If the answer is not explicitly stated in the context, say "I don't know".
"""

EXTRACTIVE_INSTRUCTION = """
Answer ONLY by quoting or closely paraphrasing the context.
Do NOT generalize, explain, or add background information.
Use the same terminology as the context.
"""


def assemble_prompt(
    query: str,
    context_chunks: List[Dict],
    system_instruction: Optional[str] = None,
    extractive_only: bool = False,
) -> str:
    """
    Assemble the final prompt string for an LLM.
    """

    system_instruction = system_instruction or DEFAULT_SYSTEM_INSTRUCTION

    # ---- instruction selection (THIS IS THE KEY CHANGE) ----
    instructions = BASE_INSTRUCTION
    if extractive_only:
        instructions += EXTRACTIVE_INSTRUCTION

    # ---- context rendering ----
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

    # ---- final prompt ----
    prompt = f"""
SYSTEM:
{system_instruction}

INSTRUCTIONS:
{instructions}

CONTEXT:
{context_block}

QUESTION:
{query}
""".strip()

    return prompt


# Extractive constraint refers to a, often automated, process of identifying, 
# defining, and lifting constraints—or limitations—from a data source, system, 
# or process to ensure that generated outputs or solutions adhere to specific rules.
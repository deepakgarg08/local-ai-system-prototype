# Assembles the final prompt sent to the LLM.
# Renders retrieved context with optional rerank scores to expose evidence strength.

from typing import List, Dict, Optional


DEFAULT_SYSTEM_INSTRUCTION = (
    "You are a precise technical assistant. "
    "Answer only using the provided context. "
    "Do not use outside knowledge."
)

BASE_INSTRUCTION = """
You MUST answer only using the provided context.
You MUST NOT use any external knowledge.
You MAY combine information from multiple parts of the context.
If the answer cannot be determined from the context, say "I don't know".
"""


EXTRACTIVE_INSTRUCTION = """
Base your answer strictly on the context.
You may paraphrase, but do not introduce new information.
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

    # ---- instruction selection ----
    instructions = BASE_INSTRUCTION
    if extractive_only:
        instructions += EXTRACTIVE_INSTRUCTION

    # ---- context rendering (STEP 20.4: score-aware) ----
    if not context_chunks:
        context_block = "No relevant context was retrieved."
    else:
        context_block_lines = []
        for idx, chunk in enumerate(context_chunks, start=1):
            text = chunk.get("text", "").strip()
            source = chunk.get("source", "unknown")
            chunk_id = chunk.get("chunk_id", "n/a")
            rerank_score = chunk.get("rerank_score", "n/a")

            context_block_lines.append(
                f"[{idx}] "
                f"(source: {source}, chunk: {chunk_id}, rerank_score: {rerank_score})\n"
                f"{text}"
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


# Extractive constraint refers to a controlled generation mode where the model
# is restricted to lifting or paraphrasing content strictly from provided sources.

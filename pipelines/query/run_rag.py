# pipelines/query/run_rag.py

from typing import List, Dict

from pipelines.query.retriever import retrieve_context_with_scores
from pipelines.query.relevance import is_context_relevant
from pipelines.prompting.assemble_prompt import assemble_prompt
from llms.registry import get_llm


def run_rag(query: str, top_k: int = 4) -> str:
    """
    End-to-end RAG execution WITH grounding enforcement.

    Flow:
        query
          → retrieve_context_with_scores
          → relevance check
          → assemble_prompt
          → unified LLM
          → answer
    """

    if not query or not query.strip():
        raise ValueError("Query must be a non-empty string")

    # 1. Retrieve context with similarity scores
    retrieved = retrieve_context_with_scores(query, k=top_k)

    # for debugging similarity scores
    # for text, score in retrieved:
    #     print(f"[DEBUG] similarity={score:.3f} | {text[:80]}...")


    # 2. Enforce grounding
    if not is_context_relevant(retrieved):
        return (
            "I don't know. "
            "The available documents do not contain "
            "relevant information to answer this question."
        )

    # 3. Strip scores before prompt assembly
    context_chunks: List[Dict] = [
        {"text": text}
        for text, _ in retrieved
    ]

    # 4. Assemble prompt
    prompt = assemble_prompt(
        query=query,
        context_chunks=context_chunks,
        system_instruction=None,
    )

    # 5. Generate answer
    llm = get_llm()
    return llm.generate(prompt)

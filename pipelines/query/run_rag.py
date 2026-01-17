# pipelines/query/run_rag.py

from typing import List, Dict

from pipelines.query.retriever import retrieve_context
from pipelines.prompting.assemble_prompt import assemble_prompt
from llms.registry import get_llm


def run_rag(query: str, top_k: int = 4) -> str:
    """
    End-to-end RAG execution.

    Flow:
        query
          → retrieve_context (FAISS)
          → assemble_prompt
          → unified LLM
          → answer
    """
    if not query or not query.strip():
        raise ValueError("Query must be a non-empty string")

    # 1. Retrieve relevant context (list[str])
    contexts: List[str] = retrieve_context(query, k=top_k)

    if all(len(c.strip()) < 20 for c in contexts):
        return "I don't know (no sufficient context found)"

    if not contexts:
        raise RuntimeError("No relevant context retrieved")

    # 2. Normalize into assemble_prompt-compatible structure
    context_chunks: List[Dict] = [
        {"text": text}
        for text in contexts
    ]

    # 3. Assemble prompt
    prompt = assemble_prompt(
        query=query,
        context_chunks=context_chunks,
        system_instruction=None,  # placeholder for future control
    )

  

    # 4. Generate answer
    llm = get_llm()
    answer = llm.generate(prompt)

    return answer

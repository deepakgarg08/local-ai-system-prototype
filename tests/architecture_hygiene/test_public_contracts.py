from pipelines.query.retriever import retrieve_context
from pipelines.query.run_rag import run_rag


def test_retrieve_context_contract():
    result = retrieve_context("test query", k=2)
    assert isinstance(result, list)


def test_run_rag_returns_string():
    answer = run_rag("What is this system?")
    assert isinstance(answer, str)

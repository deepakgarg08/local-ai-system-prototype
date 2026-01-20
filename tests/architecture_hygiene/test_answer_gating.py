from pipelines.query.run_rag import run_rag
from tests.fakes.fake_llm import FakeLLM


def test_answer_gate_can_block_llm_output(monkeypatch):
    # Fake LLM returns a clearly unsafe / hallucinated answer
    llm = FakeLLM(answer="hallucinated nonsense")

    # Monkeypatch get_llm so run_rag uses our fake
    monkeypatch.setattr(
        "pipelines.query.run_rag.get_llm",
        lambda: llm,
    )

    result = run_rag("test query")

    # Answer must be blocked by is_answer_allowed
    assert result.answer is None

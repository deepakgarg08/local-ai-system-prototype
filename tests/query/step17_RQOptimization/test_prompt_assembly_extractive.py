# tests/query/step17_RQOptimization/test_prompt_assembly_extractive.py

from pipelines.prompting.assemble_prompt import assemble_prompt


def test_extractive_instruction_is_present_when_enabled():
    prompt = assemble_prompt(
        query="What is X?",
        context_chunks=[{"text": "X is defined as Y."}],
        extractive_only=True,
    )

    assert "Answer ONLY by quoting or closely paraphrasing" in prompt


def test_extractive_instruction_not_present_when_disabled():
    prompt = assemble_prompt(
        query="What is X?",
        context_chunks=[{"text": "X is defined as Y."}],
        extractive_only=False,
    )

    assert "Answer ONLY by quoting or closely paraphrasing" not in prompt


def test_prompt_includes_rerank_score_when_present():
    prompt = assemble_prompt(
        query="What is X?",
        context_chunks=[
            {
                "text": "X is defined as Y.",
                "source": "doc1",
                "chunk_id": "c1",
                "rerank_score": 0.92,
            }
        ],
    )

    assert "rerank_score: 0.92" in prompt

def test_prompt_uses_na_when_rerank_score_missing():
    prompt = assemble_prompt(
        query="What is X?",
        context_chunks=[
            {
                "text": "X is defined as Y.",
                "source": "doc1",
                "chunk_id": "c1",
            }
        ],
    )

    assert "rerank_score: n/a" in prompt

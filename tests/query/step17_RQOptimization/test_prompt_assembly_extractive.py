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

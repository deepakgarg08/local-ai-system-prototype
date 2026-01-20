# Tests score-based answer gating behavior.
# Ensures weak evidence blocks answers deterministically.

from pipelines.gating.score_gate import ScoreThresholdGate


def test_allows_answer_when_score_is_high():
    gate = ScoreThresholdGate(min_score=0.5)

    chunks = [
        {"text": "A", "rerank_score": 0.82},
        {"text": "B", "rerank_score": 0.40},
    ]

    assert gate.allow_answer(chunks) is True


def test_blocks_answer_when_score_is_low():
    gate = ScoreThresholdGate(min_score=0.5)

    chunks = [
        {"text": "A", "rerank_score": 0.31},
        {"text": "B", "rerank_score": 0.42},
    ]

    assert gate.allow_answer(chunks) is False


def test_blocks_answer_when_no_chunks():
    gate = ScoreThresholdGate(min_score=0.5)

    assert gate.allow_answer([]) is False

from pipelines.query.relevance import is_context_relevant


def test_relevance_returns_false_for_empty_context():
    """
    Empty retrieval must always be considered irrelevant.
    """
    assert is_context_relevant([]) is False


def test_relevance_blocks_low_similarity():
    """
    Context where all chunks are below the threshold
    must be rejected.
    """
    retrieved = [
        ("some text", 0.10),
        ("another text", 0.20),
    ]

    assert is_context_relevant(retrieved) is False


def test_relevance_accepts_high_similarity():
    """
    A single strong chunk is enough to allow answering.
    """
    retrieved = [
        ("weak chunk", 0.10),
        ("strong chunk", 0.42),
    ]

    assert is_context_relevant(retrieved) is True

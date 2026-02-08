from pipelines.query.run_rag import run_rag


def test_confidence_telemetry_emitted_on_idk(monkeypatch):
    """
    STEP 21:
    Telemetry must be emitted exactly once even when
    the system answers IDK (pre-LLM grounding failure).
    """

    captured_events = []

    def fake_emit(event):
        captured_events.append(event)

    # Patch telemetry emission at the correct import location
    monkeypatch.setattr(
        "pipelines.query.run_rag.emit_confidence_event",
        fake_emit,
    )

    # Force grounding failure → IDK
    result = run_rag("this question does not exist anywhere", top_k=1)

    # --- Core behavioral assertions ---
    assert result.answer is None
    assert result.confidence is not None

    # --- Telemetry contract assertions ---
    assert len(captured_events) == 1, "Telemetry must be emitted exactly once"

    event = captured_events[0]

    assert event["answer_type"] == "IDK"
    assert event["confidence_level"].upper() == "NONE"
    assert event["model_backend"] is None

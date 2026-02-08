import json
def test_validation_event_includes_config_version(tmp_path, monkeypatch):
    # Arrange: fake config
    fake_config = {
        "version": "vTEST",
        "retrieval": {"min_similarity_threshold": 0.5},
        "corpus": {"profile": "small"},
    }

    monkeypatch.setattr(
        "configs.loader.load_active_config",
        lambda: fake_config
    )

    # Redirect log file
    from telemetry.validation_logger import LOG_FILE
    monkeypatch.setattr(
        "telemetry.validation_logger.LOG_FILE",
        tmp_path / "validation.jsonl"
    )

    # Act
    from telemetry.validation_logger import emit_validation_event
    emit_validation_event(stage="test", status="PASS")

    # Assert
    event = json.loads((tmp_path / "validation.jsonl").read_text())
    assert event["config_version"] == "vTEST"

# tests/conftest.py

import sys
import json
from pathlib import Path
import pytest


# -------------------------------------------------
# Ensure project root is on PYTHONPATH for tests
# -------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def project_root_on_path():
    project_root = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(project_root))
    return project_root


# -------------------------------------------------
# Load processed data directory
# -------------------------------------------------
@pytest.fixture(scope="session")
def processed_data_dir(project_root_on_path: Path) -> Path:
    return project_root_on_path / "data" / "processed"


# -------------------------------------------------
# Load real chunks.json (read-only)
# -------------------------------------------------
@pytest.fixture(scope="session")
def chunks_json(processed_data_dir: Path):
    with open(processed_data_dir / "chunks.json", encoding="utf-8") as f:
        return json.load(f)


# -------------------------------------------------
# Provide ONE real chunk (stable reference)
# -------------------------------------------------
@pytest.fixture(scope="session")
def real_chunk(chunks_json: list[dict]) -> dict:
    return chunks_json[0]


# -------------------------------------------------
# Provide a valid retrieval item (NEW retrieval contract)
# -------------------------------------------------
@pytest.fixture
def real_retrieval_item(real_chunk: dict) -> dict:
    return {
        "chunk_id": real_chunk["chunk_id"],
        "section_id": real_chunk["section_id"],
        "document_id": real_chunk["document_id"],
        "text": real_chunk["text"],
        "similarity": 0.55,
    }

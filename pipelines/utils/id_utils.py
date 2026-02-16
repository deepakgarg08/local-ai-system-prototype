import hashlib


def stable_hash(text: str, length: int = 16) -> str:
    """
    Generate a deterministic hash from input text.
    """
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def generate_file_id(file_path: str) -> str:
    return stable_hash(f"file::{file_path}")


def generate_document_id(file_path: str) -> str:
    return stable_hash(f"document::{file_path}")


def generate_section_id(document_id: str, section_title: str) -> str:
    base = f"section::{document_id}::{section_title}"
    return stable_hash(base)


def generate_chunk_id(document_id: str, section_id: str, chunk_index: int) -> str:
    base = f"chunk::{document_id}::{section_id}::{chunk_index}"
    return stable_hash(base)

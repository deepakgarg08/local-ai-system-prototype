from pathlib import Path
from .pdf import PDFParser

def get_parser(path: str):
    suffix = Path(path).suffix.lower()

    if suffix == ".pdf":
        return PDFParser()

    raise ValueError(f"No parser registered for {suffix}")

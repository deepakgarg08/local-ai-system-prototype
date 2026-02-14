from pathlib import Path
from docx import Document
from .base_loader import BaseDocumentLoader


class DocxLoader(BaseDocumentLoader):

    def load(self, path: Path) -> dict:
        doc = Document(path)
        text = "\n".join(p.text for p in doc.paragraphs)

        return {
            "text": text,
            "metadata": {
                "source": str(path),
                "file_type": "docx"
            }
        }

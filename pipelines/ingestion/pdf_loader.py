from pathlib import Path
from pypdf import PdfReader
from .base_loader import BaseDocumentLoader


class PdfLoader(BaseDocumentLoader):

    def load(self, path: Path) -> dict:
        reader = PdfReader(str(path))
        text = ""

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

        return {
            "text": text,
            "metadata": {
                "source": str(path),
                "file_type": "pdf",
                "num_pages": len(reader.pages)
            }
        }

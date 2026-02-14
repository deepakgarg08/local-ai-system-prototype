from pathlib import Path
from .base_loader import BaseDocumentLoader


class TxtLoader(BaseDocumentLoader):

    def load(self, path: Path) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

        return {
            "text": text,
            "metadata": {
                "source": str(path),
                "file_type": "txt"
            }
        }

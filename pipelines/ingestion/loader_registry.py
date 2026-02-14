from pathlib import Path
from .txt_loader import TxtLoader
from .pdf_loader import PdfLoader
from .docx_loader import DocxLoader
from .pptx_loader import PptxLoader


LOADERS = {
    ".txt": TxtLoader(),
    ".pdf": PdfLoader(),
    ".docx": DocxLoader(),
    ".pptx": PptxLoader(),
}


def get_loader(path: Path):
    suffix = path.suffix.lower()

    if suffix not in LOADERS:
        raise ValueError(f"No loader registered for {suffix}")

    return LOADERS[suffix]

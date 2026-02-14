import logging
import fitz
import pytesseract
from PIL import Image

from .base import BaseParser, ParsedDocument


logger = logging.getLogger(__name__)


class PDFParser(BaseParser):

    def _extract_native(self, path: str) -> str:
        doc = fitz.open(path)
        text_chunks = []

        for page in doc:
            text_chunks.append(page.get_text())

        doc.close()
        return "\n".join(text_chunks).strip()

    def _extract_ocr(self, path: str, lang: str = "deu+eng") -> str:
        doc = fitz.open(path)
        full_text = []

        for page in doc:
            pix = page.get_pixmap(dpi=300)

            img = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            text = pytesseract.image_to_string(img, lang=lang)
            full_text.append(text)

        doc.close()
        return "\n".join(full_text).strip()

    def parse(self, path: str) -> ParsedDocument:

        logger.info(f"[PDFParser] Parsing: {path}")

        native_text = self._extract_native(path)

        doc = fitz.open(path)
        page_count = doc.page_count
        doc.close()

        if len(native_text) > 200:
            logger.info("[PDFParser] Native extraction used.")

            return ParsedDocument(
                text=native_text,
                metadata={
                    "pages": page_count,
                    "method": "native"
                },
                source_path=path,
                parser_type="pdf",
                ocr_used=False
            )

        logger.info("[PDFParser] OCR fallback activated.")

        ocr_text = self._extract_ocr(path)

        return ParsedDocument(
            text=ocr_text,
            metadata={
                "pages": page_count,
                "method": "ocr"
            },
            source_path=path,
            parser_type="pdf",
            ocr_used=True
        )

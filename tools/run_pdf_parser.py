import logging
from pathlib import Path

from pipelines.indexing.parsers.registry import get_parser


# ============================================================
# Canonical project root
# ============================================================
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# ============================================================
# Source & Target Directories
# ============================================================
SOURCE_ROOT = PROJECT_ROOT / "data" / "type_of_files" / "pdf"
TARGET_ROOT = PROJECT_ROOT / "data" / "raw" / "pdf"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def main():

    if not SOURCE_ROOT.exists():
        raise FileNotFoundError(f"Source directory not found: {SOURCE_ROOT}")

    pdf_files = list(SOURCE_ROOT.rglob("*.pdf"))

    if not pdf_files:
        print("No PDF files found.")
        return

    print(f"Found {len(pdf_files)} PDF files.\n")

    total_native = 0
    total_ocr = 0

    for pdf_path in pdf_files:

        relative_path = pdf_path.relative_to(SOURCE_ROOT)

        # Replace .pdf with .txt
        output_path = TARGET_ROOT / relative_path.with_suffix(".txt")

        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        print("=" * 60)
        print(f"Processing: {relative_path}")

        parser = get_parser(str(pdf_path))
        result = parser.parse(str(pdf_path))

        # Save extracted text
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(result.text)

        if result.ocr_used:
            total_ocr += 1
        else:
            total_native += 1

        print(f"Saved to: {output_path.relative_to(PROJECT_ROOT)}")
        print(f"Pages: {result.metadata['pages']}")
        print(f"Method: {result.metadata['method']}")
        print(f"OCR Used: {result.ocr_used}")
        print(f"Text Length: {len(result.text)}")

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print(f"Total PDFs: {len(pdf_files)}")
    print(f"Native extracted: {total_native}")
    print(f"OCR used: {total_ocr}")


if __name__ == "__main__":
    main()

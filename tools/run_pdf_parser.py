import logging
import json
from pathlib import Path

from pipelines.indexing.parsers.pdf_structured_parser import parse_pdf


# ============================================================
# Logging Setup
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - [PDFParser] %(message)s"
)

logger = logging.getLogger(__name__)


# ============================================================
# Project Paths
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

SOURCE_ROOT = PROJECT_ROOT / "data" / "type_of_files" / "pdf"
OUTPUT_ROOT = PROJECT_ROOT / "data" / "raw" / "pdf"
REPORT_ROOT = PROJECT_ROOT / "data" / "reports"


# ============================================================
# Main Execution
# ============================================================

def main():

    if not SOURCE_ROOT.exists():
        raise FileNotFoundError(f"Source directory not found: {SOURCE_ROOT}")

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    REPORT_ROOT.mkdir(parents=True, exist_ok=True)

    pdf_files = list(SOURCE_ROOT.rglob("*.pdf"))

    if not pdf_files:
        logger.warning("No PDF files found.")
        return

    logger.info(f"Found {len(pdf_files)} PDF files.")

    # --------------------------------------------------------
    # Metrics Accumulators
    # --------------------------------------------------------

    report = {
        "summary": {},
        "files": []
    }

    total_files = 0
    single_column = 0
    two_column = 0
    ocr_count = 0
    total_text_length = 0

    # --------------------------------------------------------
    # Process Each PDF
    # --------------------------------------------------------

    for pdf_path in pdf_files:

        relative_path = pdf_path.relative_to(SOURCE_ROOT)
        output_path = OUTPUT_ROOT / relative_path.with_suffix(".txt")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Parsing: {pdf_path}")

        try:
            text, layout_info = parse_pdf(str(pdf_path))

            output_path.write_text(text, encoding="utf-8")

            # ------------------------------------------------
            # Existing Per-File Print Output (UNCHANGED)
            # ------------------------------------------------

            print("\n----------------------------------------")
            print(f"Processing: {relative_path}")
            print(f"Saved to: {output_path.relative_to(PROJECT_ROOT)}")
            print(f"Pages: {layout_info.get('pages', 'N/A')}")
            print("Method: native")
            print("OCR Used: False")
            print(f"Text Length: {len(text)}")
            print(f"Columns Detected: {layout_info['columns_detected']}")
            print(f"Left Blocks: {layout_info['left_blocks']}")
            print(f"Right Blocks: {layout_info['right_blocks']}")
            print("----------------------------------------\n")

            # ------------------------------------------------
            # Collect Structured Metrics
            # ------------------------------------------------

            file_entry = {
                "file_name": str(relative_path),
                "pages": layout_info.get("pages", None),
                "method": "native",
                "ocr_used": False,
                "text_length": len(text),
                "columns_detected": layout_info["columns_detected"],
                "left_blocks": layout_info["left_blocks"],
                "right_blocks": layout_info["right_blocks"]
            }

            report["files"].append(file_entry)

            total_files += 1
            total_text_length += len(text)

            if layout_info["columns_detected"] == 1:
                single_column += 1
            else:
                two_column += 1

        except Exception as e:
            logger.error(f"Failed to parse {pdf_path}: {e}")

    # --------------------------------------------------------
    # Generate Summary Metrics
    # --------------------------------------------------------

    if total_files > 0:
        report["summary"] = {
            "total_files": total_files,
            "single_column": single_column,
            "two_column": two_column,
            "ocr_used": ocr_count,
            "total_text_length": total_text_length,
            "avg_text_length": total_text_length // total_files
        }

        output_report_file = REPORT_ROOT / "pdf_parsing_report.json"

        with open(output_report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        # Keep summary visible in console
        print("\n===== PDF Parsing Summary =====")
        print(json.dumps(report["summary"], indent=2))
        print(f"\nReport saved to: {output_report_file}")
        print("================================\n")


if __name__ == "__main__":
    main()

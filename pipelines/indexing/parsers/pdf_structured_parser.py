import fitz
from pipelines.indexing.parsers.layout_analyzer import analyze_layout


def extract_text_page(page):
    """
    Extract text from a single page using block-level
    reading order reconstruction.

    Works for:
    - single column
    - two column
    - mixed layouts
    """

    blocks = page.get_text("blocks")

    # Sort by vertical position (y0), then horizontal (x0)
    blocks_sorted = sorted(blocks, key=lambda b: (b[1], b[0]))

    # Extract block text (index 4 contains text)
    text = "\n".join(b[4] for b in blocks_sorted)

    return text


def parse_pdf(pdf_path: str):
    """
    Parse a PDF file and return structured metadata
    along with reconstructed full text.
    """

    doc = fitz.open(pdf_path)

    layout_info = analyze_layout(pdf_path)
    num_columns = layout_info.get("columns_detected", 1)

    full_text = []

    for page in doc:
        text = extract_text_page(page)
        full_text.append(text)

    doc.close()

    combined_text = "\n\n".join(full_text)

    return {
        "file": pdf_path,
        "pages": len(full_text),
        "method": "block_sorted_reading_order",
        "ocr_used": False,
        "text_length": len(combined_text),
        "columns_detected": num_columns,
        "text": combined_text,
    }

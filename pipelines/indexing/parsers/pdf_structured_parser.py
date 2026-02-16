import fitz
from pipelines.indexing.parsers.layout_analyzer import analyze_layout

def extract_text_single_column(page):
    return page.get_text("text")


def extract_text_two_column(page):
    blocks = page.get_text("blocks")
    page_width = page.rect.width

    left = []
    right = []

    for block in blocks:
        x0, y0, x1, y1, text, *_ = block
        center_x = (x0 + x1) / 2

        if center_x < page_width / 2:
            left.append((y0, text))
        else:
            right.append((y0, text))

    left.sort(key=lambda x: x[0])
    right.sort(key=lambda x: x[0])

    left_text = "\n".join(t for _, t in left)
    right_text = "\n".join(t for _, t in right)

    return left_text + "\n\n" + right_text


def parse_pdf(pdf_path: str):
    doc = fitz.open(pdf_path)

    layout_info = analyze_layout(pdf_path)
    num_columns = layout_info["columns_detected"]

    full_text = []

    for page in doc:
        if num_columns == 1:
            text = extract_text_single_column(page)
        else:
            text = extract_text_two_column(page)

        full_text.append(text)

        return {
                "file": path,
                "pages": pages,
                "method": method,
                "ocr_used": ocr_used,
                "text_length": len(text),
                "columns_detected": columns,
                "left_blocks": left_blocks,
                "right_blocks": right_blocks,
        }
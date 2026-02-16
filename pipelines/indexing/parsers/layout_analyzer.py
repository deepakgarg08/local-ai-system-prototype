import fitz
import statistics


def analyze_layout(pdf_path: str) -> dict:
    doc = fitz.open(pdf_path)

    centers = []
    pages_to_check = min(5, len(doc))

    for i in range(1, pages_to_check):  # skip title page
        page = doc[i]
        blocks = page.get_text("blocks")

        for block in blocks:
            x0, y0, x1, y1, text, *_ = block
            if text.strip():
                center_x = (x0 + x1) / 2
                centers.append(center_x)

    if len(centers) < 10:
        return {
            "columns_detected": 1,
            "left_blocks": 0,
            "right_blocks": 0,
            "pages_analyzed": pages_to_check
        }

    min_x = min(centers)
    max_x = max(centers)
    spread = max_x - min_x

    median_x = statistics.median(centers)

    left = [c for c in centers if c < median_x]
    right = [c for c in centers if c >= median_x]

    # Compute cluster separation
    if left and right:
        separation = abs(statistics.mean(right) - statistics.mean(left))
    else:
        separation = 0

    # If separation is large relative to spread → 2 columns
    if separation > spread * 0.4:
        columns = 2
    else:
        columns = 1

    return {
        "columns_detected": columns,
        "left_blocks": len(left),
        "right_blocks": len(right),
        "pages_analyzed": pages_to_check
    }

def format_sources(evidence):
    lines = []
    seen = set()

    for e in evidence:
        key = (e.source_document, e.section_title)
        if key in seen:
            continue
        seen.add(key)

        lines.append(
            f"- {e.source_document}"
            + (f" | section: {e.section_title}" if e.section_title else "")
            + (f" | file: {e.file_path}" if e.file_path else "")
        )

    return "\n".join(lines)

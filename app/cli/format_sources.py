def format_sources(evidence):
    lines = []
    seen = set()

    for e in evidence:
        key = (e.source_document, e.section_title)
        if key in seen:
            continue
        seen.add(key)

        # lines.append(
        #     f"- {e.source_document}"
        #     + (f" | section: {e.section_title}" if e.section_title else "")
        #     + (f" | file: {e.file_path}" if e.file_path else "")
        # )

        #  debug mode: show more details about each source
        lines.append(
                f"- File: {e.file_path}\n"
                f"  Document: {e.source_document}\n"
                f"  Section: {e.section_title}\n"
                f"  Chunk ID: {e.chunk_id}\n"
                f"  Similarity: {e.similarity_score:.3f}\n"
            )

    return "\n".join(lines)

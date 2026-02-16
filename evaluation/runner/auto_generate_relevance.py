import json
from pathlib import Path
from pipelines.query.retriever import retrieve_context_structured


PROJECT_ROOT = Path(__file__).resolve().parents[2]

QUERIES_PATH = PROJECT_ROOT / "evaluation" / "datasets" / "golden_queries.json"
OUTPUT_PATH = PROJECT_ROOT / "evaluation" / "datasets" / "relevance_judgments.json"


def keyword_match(expected_keyword: str, text: str) -> bool:
    """
    Loose keyword matching:
    All words in expected_keyword must appear in text.
    """
    words = expected_keyword.lower().split()
    text = text.lower()
    return all(word in text for word in words)


def main():

    with open(QUERIES_PATH, "r", encoding="utf-8") as f:
        queries = json.load(f)

    relevance = {}

    for q in queries:
        qid = q["id"]
        query_text = q["query"]
        expected_keyword = q.get("expected_keyword", "").strip()

        if not expected_keyword:
            relevance[qid] = []
            continue

        retrieved_chunks = retrieve_context_structured(query_text, k=5)

        matched_ids = []

        for chunk in retrieved_chunks:
            full_text = chunk["text"]

            if keyword_match(expected_keyword, full_text):
                matched_ids.append(chunk["id"])

        relevance[qid] = matched_ids

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(relevance, f, indent=2)

    print("Relevance judgments auto-generated successfully.")


if __name__ == "__main__":
    main()

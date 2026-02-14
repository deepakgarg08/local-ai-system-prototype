from pathlib import Path
from .loader_registry import get_loader


def ingest_directory(directory: Path):
    documents = []

    for path in directory.rglob("*"):
        if path.is_file():
            try:
                loader = get_loader(path)
                doc = loader.load(path)
                documents.append(doc)
                print(f"Loaded: {path}")
            except ValueError:
                # Unsupported file type
                continue
            except Exception as e:
                print(f"Failed to load {path}: {e}")

    return documents


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m pipelines.ingestion.ingest_documents <directory>")
        sys.exit(1)

    target_dir = Path(sys.argv[1])
    docs = ingest_directory(target_dir)

    print(f"Total documents ingested: {len(docs)}")

import subprocess
import sys


STAGES = [
    "tools.run_pdf_parser",
    "pipelines.ingestion.ingest_txt",
    "pipelines.chunking.chunk_sections",
    "pipelines.indexing.build_index",            # Chunk-level index
    "pipelines.indexing.build_document_index",  # STEP 34: Document-level index
    "evaluation.runner.run_retrieval_eval",
]


def run_stage(module: str):
    print(f"\n=== Running: {module} ===\n")
    result = subprocess.run(
        ["uv", "run", "python", "-m", module],
        check=False,
    )

    if result.returncode != 0:
        print(f"\n❌ Stage failed: {module}")
        sys.exit(result.returncode)


def main():
    print("\n🚀 Starting ETL Pipeline\n")

    for stage in STAGES:
        run_stage(stage)

    print("\n✅ ETL Pipeline Completed Successfully\n")


if __name__ == "__main__":
    main()

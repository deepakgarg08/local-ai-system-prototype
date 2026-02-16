first add data to data/raw folder
if the data is pdf run this `tools/run_pdf_parser.py`
then run 
<!-- uvp = uv python -m -->
uv run python -m tools.run_pdf_parser
uv run python -m pipelines.ingestion.ingest_txt
uv run python -m pipelines.chunking.chunk_sections
uv run python -m pipelines.indexing.build_index
uv run python -m evaluation.runner.run_retrieval_eval


python run_pdf_parser.py

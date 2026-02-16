first add data to data/raw folder
if the data is pdf run this `tools/run_pdf_parser.py`
then run 
<!-- uvp = uv python -m -->
python pipelines/ingestion/ingest_txt.py
python pipelines/chunking/chunk_sections.py
python pipelines/indexing/build_index.py
uvp evaluation.runner.run_retrieval_eval

python run_pdf_parser.py




import sys
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()  # loads .env into os.environ

print(os.getenv("LLM_PROVIDER"))
print(os.getenv("LLM_MODEL"))
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st
from pipelines.query.run_rag import run_rag

st.set_page_config(
    page_title="Local AI Assistant",
    layout="centered",
)

st.title("Local AI Assistant")
st.caption("Document-grounded answers only")

# UI-only history (never fed back into RAG)
if "history" not in st.session_state:
    st.session_state.history = []

with st.form(key="query_form"):
    query = st.text_input(
        label="Enter your question",
        placeholder="e.g. termination policy",
    )
    submitted = st.form_submit_button("Ask")

if submitted and query.strip():
    result = run_rag(query=query, top_k=5)

    if result.answer:
        answer_text = result.answer
    else:
        answer_text = "No sufficiently grounded answer found."

    st.session_state.history.append((query, answer_text))


# Render history (latest first)
for q, a in reversed(st.session_state.history):
    st.markdown(f"**You:** {q}")
    st.markdown(f"**Assistant:** {a}")
    st.markdown("---")

from pipelines.prompting import assemble_prompt

# from pipelines.prompting import assemble_prompt

query = "What is cosine similarity?"

context_chunks = [
    {
        "text": "Cosine similarity measures the cosine of the angle between two vectors.",
        "source": "nlp_basics.pdf",
        "chunk_id": 12,
    },
    {
        "text": "It is commonly used in information retrieval and NLP tasks.",
        "source": "search_notes.txt",
        "chunk_id": 4,
    },
]

prompt = assemble_prompt(query, context_chunks)

print(prompt)
# from pipelines.prompting import assemble_prompt
# from pipelines.llm import LocalLLM, OnlineLLM


# def main():
#     query = "What is cosine similarity?"

#     context_chunks = [
#         {
#             "text": "Cosine similarity measures the cosine of the angle between two vectors.",
#             "source": "nlp_basics.pdf",
#             "chunk_id": 12,
#         }
#     ]

#     prompt = assemble_prompt(query, context_chunks)

#     local_llm = LocalLLM()
#     online_llm = OnlineLLM(provider="openai")

#     print("=== LOCAL LLM ===")
#     print(local_llm.generate(prompt))

#     print("\n=== ONLINE LLM ===")
#     print(online_llm.generate(prompt))


# if __name__ == "__main__":
#     main()

# from llms.ollama import OllamaLLM

# llm = OllamaLLM(model="deepseek-coder:6.7b")

# response = llm.generate(
#     "Explain what a vector database is in one concise paragraph."
# )

# print(response)

#  Above was earlier smog test code to check if ollama llm was working fine.

# pipelines/llm/test_llm_interface.py

from llms.registry import get_llm

llm = get_llm()

response = llm.generate(
    "Explain what a vector database is in one concise paragraph."
)

print(response)

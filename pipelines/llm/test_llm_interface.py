from llms.ollama import OllamaLLM

llm = OllamaLLM(model="deepseek-coder:6.7b")

response = llm.generate(
    "Explain what a vector database is in one concise paragraph."
)

print(response)

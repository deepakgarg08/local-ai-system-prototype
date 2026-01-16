from ollama import chat

response = chat(
    model="deepseek-coder:6.7b",
    messages=[
        {"role": "user", "content": "Explain what a vector database is in one concise paragraph."}
    ]
)

print(response["message"]["content"])

from ollama import chat
from llms.base import BaseLLM


class OllamaLLM(BaseLLM):
    def __init__(self, model: str):
        self.model = model

    def generate(self, prompt: str) -> str:
        response = chat(
            model=self.model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response["message"]["content"]

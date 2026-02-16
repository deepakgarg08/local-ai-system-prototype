from ollama import chat
from llms.base import BaseLLM
import signal


class OllamaLLM(BaseLLM):
    def __init__(self, model: str):
        self.model = model

from ollama import chat
from llms.base import BaseLLM


class OllamaLLM(BaseLLM):
    def __init__(self, model: str):
        self.model = model

    def generate(self, prompt: str) -> str:
        try:
            response = chat(
                model=self.model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                options={
                    "num_predict": 512,
                },
            )

            return response["message"]["content"]

        except Exception:
            return (
                "I don't know.\n"
                "The language model failed to respond."
            )


        finally:
            # Always disable the alarm
            signal.alarm(0)

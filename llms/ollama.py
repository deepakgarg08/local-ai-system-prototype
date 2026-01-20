from ollama import chat
from llms.base import BaseLLM
import signal


class OllamaLLM(BaseLLM):
    def __init__(self, model: str):
        self.model = model

    def generate(self, prompt: str) -> str:
        def timeout_handler(signum, frame):
            raise TimeoutError("LLM call timed out")

        # Set a 30s alarm (Unix / Linux only)
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(30)

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

        except TimeoutError:
            return (
                "I don't know.\n"
                "The language model did not respond in time."
            )

        except Exception as e:
            return (
                "I don't know.\n"
                "The language model failed to respond."
            )

        finally:
            # Always disable the alarm
            signal.alarm(0)

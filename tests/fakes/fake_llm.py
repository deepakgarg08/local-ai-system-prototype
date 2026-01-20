from llms.base import BaseLLM


class FakeLLM(BaseLLM):
    """
    Deterministic fake LLM for tests.

    Allows tests to control exactly what the model returns,
    without environment variables, network calls, or real models.
    """

    def __init__(self, answer: str = "fake answer"):
        self._answer = answer

    def generate(self, prompt: str) -> str:
        return self._answer

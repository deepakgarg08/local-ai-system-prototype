from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    Abstract base class for all LLM backends.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a completion for a given prompt.

        Args:
            prompt (str): Input prompt

        Returns:
            str: Model-generated text
        """
        raise NotImplementedError

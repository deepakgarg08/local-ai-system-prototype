# pipelines/llm/base.py

from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    Abstract base class for all LLM connectors.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response for the given prompt.

        Parameters
        ----------
        prompt : str
            Fully assembled prompt

        Returns
        -------
        str
            Model-generated response
        """
        pass

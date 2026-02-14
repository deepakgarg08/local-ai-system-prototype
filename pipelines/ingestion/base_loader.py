from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict


class BaseDocumentLoader(ABC):

    @abstractmethod
    def load(self, path: Path) -> Dict:
        """
        Returns:
            {
                "text": str,
                "metadata": dict
            }
        """
        pass

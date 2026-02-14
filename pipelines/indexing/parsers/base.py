from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict


@dataclass
class ParsedDocument:
    text: str
    metadata: Dict
    source_path: str
    parser_type: str
    ocr_used: bool = False


class BaseParser(ABC):

    @abstractmethod
    def parse(self, path: str) -> ParsedDocument:
        pass

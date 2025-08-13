from abc import ABC, abstractmethod
from pathlib import Path
from typing import List

class Embedder(ABC):
    @abstractmethod
    def embed(self, texts: List[str]) -> List[List[float]]:
        pass

    @abstractmethod
    def embed_and_store(self, paper_id: str, chunks: List[str]):
        pass
    
    @staticmethod
    @abstractmethod
    def load_vectors_from_json(json_path: Path) -> tuple[str, list[float]]:
        pass
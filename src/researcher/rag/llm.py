from abc import ABC, abstractmethod
from typing import Optional


class LLMInference(ABC):
    @abstractmethod
    def ask(self, prompt: str, system_prompt: Optional[str] = None, options: dict = None) -> str:
        pass
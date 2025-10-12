from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """
    Base interface for all agents.
    """

    @abstractmethod
    def run(self, prompt: dict) -> dict:
        NotImplemented("The agent class should implement this!")

from abc import ABC, abstractmethod
from pathlib import Path


class BasicDownloadTool(ABC):
    """
    Base interface for download tools.
    """

    @abstractmethod
    def download(self, url: str) -> Path:
        NotImplemented("The downloader class should implement this!")
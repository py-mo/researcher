from abc import ABC, abstractmethod
from pathlib import Path


class BasicDownloadTool(ABC):
    """
    Base interface for download tools.
    """

    @abstractmethod
    async def download(self, url: str) -> Path:
        NotImplemented("The downloader class should implement this!")
    
    @abstractmethod
    async def get_pdf_url(self, abs_url: str) -> Path:
        NotImplemented("The downloader class should implement this!")
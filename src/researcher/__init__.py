__version__ = "0.1.0"

from .integrations.arxiv_search import ArxivSearch
from .integrations.arxiv_downloader import ArxivDownloader
from .storage.folder_manager import FolderManager
from .cli.cli import main
from .extract.pdf_text import PDFTextExtractor
from .embedding import NomicEmbedder, simple_chunk, EmbeddingSearcher

__all__ = ["ArxivSearch", "ArxivDownloader", "FolderManager"
           , "PDFTextExtractor", "main"
           , "NomicEmbedder", "simple_chunk"
           , "EmbeddingSearcher"]

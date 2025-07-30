__version__ = "0.1.0"

from .integrations import ArxivSearch
from .integrations import ArxivDownloader
from .storage import FolderManager
from .cli import main
from .extract import PDFTextExtractor
from .embedding import NomicEmbedder, simple_chunk, EmbeddingSearcher

__all__ = ["ArxivSearch", "ArxivDownloader", "FolderManager"
           , "PDFTextExtractor", "main"
           , "NomicEmbedder", "simple_chunk"
           , "EmbeddingSearcher"]

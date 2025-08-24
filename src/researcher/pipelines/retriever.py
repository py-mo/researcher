from pathlib import Path
from typing import List
from researcher import EmbeddingSearcher
from researcher.embedding.index_builder import build_annoy_index
from researcher.embedding import Embedder


class RetrieverPipeline:
    def __init__(self, embedder: Embedder, embeddings_path: List[Path], index_path: Path, mapping_path: Path
                 , dim: int, n_trees: int):
        self.embeddings_path = embeddings_path
        self.index_path = index_path
        self.mapping_path = mapping_path
        self.dim = dim
        self.n_trees = n_trees
        self.embedder = embedder
        
        self.search_loader = EmbeddingSearcher(dim=dim, index_path=self.index_path, mapping_path=self.mapping_path)
        
        if not self.index_path.exists() or not self.mapping_path.exists():
            self._build_index()

    def _build_index(self):
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        
        for embedding_path in self.embeddings_path:
            build_annoy_index(
                json_path=embedding_path,
                index_dir=self.index_path.parent,
                dim=self.dim,
                n_trees=self.n_trees
            )

    def run_pipeline(self, query: str, k_neighbors: int) -> List[str]:
        self.search_loader.load()

        query_embed = self.embedder.embed(query)
        most_similar_embeddings = self.search_loader.search(query_vector=query_embed[0], k=k_neighbors)
        return most_similar_embeddings
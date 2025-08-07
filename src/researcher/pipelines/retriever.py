from pathlib import Path
from typing import List
from researcher import EmbeddingSearcher, NomicEmbedder


class RetrieverPipeline:
    def __init__(self, embeddings_path: List[Path], index_path: Path, mapping_path: Path
                 , dim: int, n_trees: int):
        self.embeddings_path = embeddings_path
        self.index_path = index_path
        self.mapping_path = mapping_path
        self.vectors: List[List[float]] = []
        self.embedder = NomicEmbedder()

        search_builder = EmbeddingSearcher(dim=dim, index_path=self.index_path, mapping_path=self.mapping_path)
        for embedding_path in self.embeddings_path:
            x = NomicEmbedder.load_vectors_from_json(embedding_path)
            self.vectors.append(x)

        search_builder.build(self.vectors, n_trees=n_trees)
        
        self.search_loader = EmbeddingSearcher(dim=dim, index_path=self.index_path, mapping_path=self.mapping_path)

    def run_pipeline(self, query: str, k_neighbors: int) -> List[str]:
        self.search_loader.load()

        query_embed = self.embedder.embed(query)
        most_similar_embeddings = self.search_loader.search(query_vector=query_embed[0], k=k_neighbors)
        return most_similar_embeddings
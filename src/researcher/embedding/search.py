from annoy import AnnoyIndex
import numpy as np
from pathlib import Path
import json


class EmbeddingSearcher:
    def __init__(self, dim: int, index_path: Path, mapping_path: Path):
        self.dim = dim
        self.index = AnnoyIndex(dim, 'angular')
        self.index_path = index_path
        self.mapping_path = mapping_path
        self.mapping = {}

    def build(self, vectors: list[tuple[str, list[float]]], n_trees=10):
        for i, (paper_id, vector) in enumerate(vectors):
            self.index.add_item(i, vector)
            self.mapping[i] = paper_id
        self.index.build(n_trees)
        self.index.save(str(self.index_path))
        with open(self.mapping_path, "w") as f:
            json.dump(self.mapping, f)

    def load(self):
        self.index.load(str(self.index_path))
        with open(self.mapping_path) as f:
            self.mapping = json.load(f)

    def search(self, query_vector: list[float], k=5):
        ids = self.index.get_nns_by_vector(query_vector, k)
        return [self.mapping[str(i)] for i in ids]
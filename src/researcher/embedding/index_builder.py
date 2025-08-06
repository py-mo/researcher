from pathlib import Path
import json
from annoy import AnnoyIndex

def build_annoy_index(json_path: Path, index_dir: Path, dim: int, n_trees=10):
    with open(json_path) as f:
        data = json.load(f)

    annoy_index = AnnoyIndex(dim, 'angular')

    vector = data[0]["embedding"]
    annoy_index.add_item(1, vector[0])

    index_dir.mkdir(parents=True, exist_ok=True)
    index_path = index_dir / "index.ann"

    annoy_index.build(n_trees)
    annoy_index.save(str(index_path))
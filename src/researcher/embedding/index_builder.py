from pathlib import Path
import json
from annoy import AnnoyIndex

def build_annoy_index(json_path: Path, index_dir: Path, dim: int, n_trees=10):
    with open(json_path) as f:
        data = json.load(f)

    annoy_index = AnnoyIndex(dim, 'angular')
    mapping = {}

    for i, item in enumerate(data):
        vector = item["embedding"]
        annoy_index.add_item(i, vector)
        mapping[i] = {
            "paper_id": item["paper_id"],
            "chunk": item["chunk"],
            "title": item["title"]
        }

    index_dir.mkdir(parents=True, exist_ok=True)
    index_path = index_dir / "annoy_index.ann"
    mapping_path = index_dir / "annoy_mapping.json"

    annoy_index.build(n_trees)
    annoy_index.save(str(index_path))
    
    with open(mapping_path, "w") as f:
        json.dump(mapping, f, indent=2)
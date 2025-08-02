import json
import requests
from pathlib import Path
from typing import List


class NomicEmbedder:
    def __init__(self, model: str = "nomic-embed-text", base_url: str = "http://localhost:11434"):
        self.model = model
        self.api_url = f"{base_url}/api/embeddings"

    def embed(self, texts: List[str]) -> List[List[float]]:
        if not texts or not all(isinstance(t, str) for t in texts):
            raise ValueError("`texts` must be a non-empty list of strings")

        embedding: list[list[float]] = []
        for text in texts:
            response = requests.post(
                self.api_url,
                json={
                    "model": self.model,
                    "prompt": text
                }
            )

            if response.status_code != 200:
                raise RuntimeError(f"Embedding failed: {response.text}")

            try:
                data = response.json()
                embedding.append(data["embedding"] if "embedding" in data else [d["embedding"] for d in data["data"]])
            except (ValueError, KeyError) as e:
                raise RuntimeError(f"Failed to parse embedding response: {e}")
        
        return embedding

    def embed_and_store(self, paper_id: str, chunks: List[str], out_dir: Path):
        vectors = self.embed(chunks)
        output = [{"text": t, "embedding": e} for t, e in zip(chunks, vectors)]

        file_path = out_dir / f"{paper_id}.json"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
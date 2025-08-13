import json
from pathlib import Path
from typing import List
import ollama
from researcher import FolderManager, Embedder


class OllamaEmbedder(Embedder):
    def __init__(self, model: str = "nomic-embed-text", papers_dir: Path = None, metadata_dir: Path = None):
        self.model = model
        self.papers_dir = papers_dir if papers_dir else Path("data/papers");
        self.metadata_dir = metadata_dir
        self.folder_manager = FolderManager(self.papers_dir, self.metadata_dir)

    def embed(self, texts: List[str]) -> List[List[float]]:
        if not texts or not all(isinstance(t, str) for t in texts):
            raise ValueError("`texts` must be a non-empty list of strings")

        embedding: list[list[float]] = []
        for text in texts:
            try:
                response = ollama.embeddings(model=self.model, prompt=text)
                embedding.append(response['embedding'])
            except Exception as e:
                raise RuntimeError(f"Embedding failed: {str(e)}")
        
        return embedding

    def embed_and_store(self, paper_id: str, chunks: List[str]
                        , out_dir: Path):
        vectors = self.embed(chunks)
        title = self.folder_manager.get_paper_info(paper_id)["title"]
        output = []
        for chunk, vector in zip(chunks, vectors):
            output.append({
                "title": title,
                "paper_id": paper_id,
                "chunk": chunk,
                "embedding": vector
            })

        file_path = out_dir / f"{paper_id}.json"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    
    @staticmethod
    def load_vectors_from_json(json_path: Path) -> tuple[str, list[float]]:
        with open(json_path) as f:
            data = json.load(f)

        vector = data[0]["embedding"]
        title = data[0]["title"]

        return [title, vector]
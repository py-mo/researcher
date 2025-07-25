import json
import subprocess
from pathlib import Path
from typing import List

class NomicEmbedder:
    def __init__(self, model: str = "nomic-embed-text"):
        self.model = model

    def embed(self, texts: List[str]) -> List[List[float]]:
        prompt = {
            "model": self.model,
            "prompt": texts,
            "stream": False
        }

        input_file = Path("data/embedding/embedding_input.json")
        input_file.write_text(json.dumps(prompt), encoding="utf-8")

        result = subprocess.run(
            ["ollama", "run", self.model, "<", str(input_file)],
            shell=True,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            raise RuntimeError(f"Ollama embedding failed: {result.stderr}")

        response = json.loads(result.stdout)
        return response["data"]

    def embed_and_store(self, paper_id: str, chunks: List[str], out_dir: Path):
        vectors = self.embed(chunks)
        output = [{"text": t, "embedding": e} for t, e in zip(chunks, vectors)]

        file_path = out_dir / f"{paper_id}.json"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
from pathlib import Path
import json


class FolderManager:
    def __init__(self, papers_dir: Path = Path("data/papers"), metadata_dir: Path = None):
        self.papers_dir = papers_dir
        self.metadata_dir = metadata_dir
        self._setup_folders()

    def _setup_folders(self):
            self.papers_dir.mkdir(parents=True, exist_ok=True)
            if self.metadata_dir: self.metadata_dir.mkdir(parents=True, exist_ok=True);

    def get_paper_path(self, paper_id: str) -> Path:
        return self.papers_dir / f"{paper_id}.pdf"

    def get_paper_info(self, paper_id: str) -> dict:
        if not self.metadata_dir: return {"title": paper_id};
        with open(self.metadata_dir / f"{paper_id}.json") as f:
            data = json.load(f)
        return data
        


if __name__ == "__main__":
    folder_manager = FolderManager()
    paper_path = folder_manager.get_paper_path("1706.03762")

    print(f"Paper Path: {paper_path}")
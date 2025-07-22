from pathlib import Path


class FolderManager:
    def __init__(self, base_dir: Path = Path("data")):
        self.base_dir = base_dir
        self.papers_dir = self.base_dir / "papers"
        self._setup_folders()

    def _setup_folders(self):
        for folder in [self.papers_dir]:
            folder.mkdir(parents=True, exist_ok=True)

    def get_paper_path(self, paper_id: str) -> Path:
        return self.papers_dir / f"{paper_id}.pdf"


if __name__ == "__main__":
    folder_manager = FolderManager()
    paper_path = folder_manager.get_paper_path("1706.03762")

    print(f"Paper Path: {paper_path}")
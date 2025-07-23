from pathlib import Path
from typing import Optional
import pypdf


class PDFTextExtractor:
    def __init__(self, file_path: Path):
        if not file_path.exists() or not file_path.suffix == ".pdf":
            raise ValueError(f"Invalid PDF file: {file_path}")
        self.file_path = file_path

    def extract_text(self) -> Optional[str]:
        try:
            with open(self.file_path, "rb") as f:
                reader = pypdf.PdfReader(f)
                text = []
                for page in reader.pages:
                    content = page.extract_text()
                    if content:
                        text.append(content)
            return "\n".join(text) if text else None
        except Exception as e:
            print(f"[ERROR] Failed to extract from {self.file_path}: {e}")
            return None
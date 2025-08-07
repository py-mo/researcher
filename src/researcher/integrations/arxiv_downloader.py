import requests
from pathlib import Path
from urllib.parse import urlparse
import json


class ArxivDownloader:
    def __init__(self, download_dir: Path = Path("data/papers"), metadata_dir: Path = None, print_msg: bool = False):
        self.download_dir = download_dir
        self.download_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir = metadata_dir
        if metadata_dir:
            self.metadata_dir.mkdir(parents=True, exist_ok=True)
        self.print_msg = print_msg

    def get_pdf_url(self, arxiv_abs_url: str) -> str:
        parsed = urlparse(arxiv_abs_url)
        pdf_url = parsed.geturl().replace("/abs/", "/pdf/") + ".pdf"
        return pdf_url

    def download_pdf(self, arxiv_abs_url: str, entries: dict = None) -> Path:
        pdf_url = self.get_pdf_url(arxiv_abs_url)
        arxiv_id = pdf_url.split("/")[-1].replace(".pdf", "")
        file_path = self.download_dir / f"{arxiv_id}.pdf"

        if file_path.exists():
            if self.print_msg: print(f"✔ PDF already downloaded: {file_path}");
            return file_path

        response = requests.get(pdf_url)
        if response.status_code == 200:
            file_path.write_bytes(response.content)
            if self.print_msg: print(f"✅ Downloaded: {file_path}");
        else:
            raise Exception(f"Failed to download PDF: {pdf_url} | Status: {response.status_code}")

        if self.metadata_dir:
            metadata_path = self.metadata_dir / f"{arxiv_id}.json"
            metadata_path.write_text(json.dumps(entries, indent=2), encoding="utf-8")
        
        return file_path


if __name__ == "__main__":
    downloader = ArxivDownloader(print_msg=True, metadata_dir=Path("data/metadata"))
    pdf_path = downloader.download_pdf("https://arxiv.org/pdf/1706.03762", {"field": "AI"})
    print(f"Saved to: {pdf_path}")
import httpx
import asyncio
import json
from pathlib import Path
from urllib.parse import urlparse
from core import BasicDownloadTool


class ArxivDownloader(BasicDownloadTool):
    """
    Arxiv Downloader
    """


    def __init__(
        self,
        download_dir: Path = Path("data/papers"),
        metadata_dir: Path | None = None,
        print_msg: bool = False
    ):
        self.download_dir = download_dir
        self.download_dir.mkdir(parents=True, exist_ok=True)

        self.metadata_dir = metadata_dir
        if metadata_dir:
            self.metadata_dir.mkdir(parents=True, exist_ok=True)

        self.print_msg = print_msg

    async def get_pdf_url(self, abs_url: str) -> str:
        """
        Convert an arXiv abstract URL to its PDF URL.
        """
        parsed = urlparse(abs_url)
        pdf_url = parsed.geturl().replace("/abs/", "/pdf/")
        return pdf_url

    async def download(self, abs_url: str, entries: dict | None = None) -> Path:
        """
        Download an arXiv PDF asynchronously given the abstract URL.
        """
        pdf_url = await self.get_pdf_url(abs_url)
        arxiv_id = pdf_url.split("/")[-1].replace(".pdf", "")
        file_path = self.download_dir / f"{arxiv_id}.pdf"

        if file_path.exists():
            if self.print_msg:
                print(f"✔ PDF already downloaded: {file_path}")
            return file_path

        async with httpx.AsyncClient() as client:
            response = await client.get(pdf_url)
            if response.status_code != 200:
                raise Exception(f"Failed to download PDF: {pdf_url} | Status: {response.status_code}")
            content = response.content

        file_path.write_bytes(content)
        if self.print_msg:
            print(f"✅ Downloaded: {file_path}")

        if self.metadata_dir and entries:
            metadata_path = self.metadata_dir / f"{arxiv_id}.json"
            metadata_path.write_text(json.dumps(entries, indent=2), encoding="utf-8")

        return file_path


if __name__ == "__main__":
    async def main():
        downloader = ArxivDownloader(print_msg=True, metadata_dir=Path("data/metadata"))
        pdf_path = await downloader.download(
            "https://arxiv.org/abs/2501.16513",
            {"field": "AI"}
        )
        print(f"Saved to: {pdf_path}")

    asyncio.run(main())

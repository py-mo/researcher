from researcher import ArxivSearch, ArxivDownloader
from pathlib import Path


class FetchPapersPipeline:
    def __init__(self, query: str, max_results: int = 5
                 , path: Path = Path("data/papers/")): 
        self.query = query
        self.path = path
        self.max_results = max_results

    def run_pipeline(self):
        results: list = ArxivSearch(query=self.query, max_results=self.max_results).search()
        downloader: ArxivDownloader = ArxivDownloader(download_dir=self.path)
        for res in results:
            downloader.download_pdf(res["link"])
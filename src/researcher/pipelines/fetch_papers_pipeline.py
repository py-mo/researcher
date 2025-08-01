from researcher import ArxivSearch, ArxivDownloader
from pathlib import Path


class FetchPapersPipeline:
    def __init__(self, query: str, max_results: int = 5
                 , path: Path = None): 
        self.query = query
        self.path = path if path else Path(f"data/papers/{query}")
        self.max_results = max_results

    def run_pipeline(self, raise_err: bool = False):
        try:
            results: list = ArxivSearch(query=self.query, max_results=self.max_results).search()
            downloader: ArxivDownloader = ArxivDownloader(download_dir=self.path)
        except Exception as e:
            print(f"Failed to fetch papers.\n{str(e)}")
            if raise_err: raise e;
        else:
            for res in results:
                downloader.download_pdf(res["link"])
from researcher import ArxivSearch, ArxivDownloader
from pathlib import Path


class FetchPapersPipeline:
    def __init__(self, query: str, max_results: int = 5
                 , output_path: Path = None, metadata_path: Path = None):
        self.query = query
        self.max_results = max_results
        if (output_path != None) and (str(output_path) != "None"):
             self.output_path = output_path
        else:
            self.output_path = Path(f"data/papers/{query}/")
        if (metadata_path != None) and (str(metadata_path) != "None"):
             self.metadata_path = metadata_path
        else:
            self.metadata_path = Path(f"data/metadata/{query}/")

    def run_pipeline(self, raise_err: bool = False):
        try:
            results: list = ArxivSearch(query=self.query, max_results=self.max_results).search()
            downloader: ArxivDownloader = ArxivDownloader(download_dir=self.output_path
                                                          , metadata_dir=self.metadata_path)
        except Exception as e:
            print(f"Failed to fetch papers.\n{str(e)}")
            if raise_err: raise e;
        else:
            for res in results:
                downloader.download_pdf(res["link"], entries=res)
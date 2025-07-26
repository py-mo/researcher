import pytest
from researcher import ArxivSearch, ArxivDownloader
from pathlib import Path


@pytest.fixture(scope="module")
def test_search_results():
    search = ArxivSearch("transformers", max_results=1)
    results = search.search()
    assert results, "No results found for test query"
    return results


def test_search_returns_title(test_search_results):
    assert "title" in test_search_results[0], "Missing title in result"


def test_download_pdf(tmp_path, test_search_results):
    downloader = ArxivDownloader(download_dir=tmp_path)
    link = test_search_results[0]["link"]
    pdf_path = downloader.download_pdf(link)
    assert pdf_path.exists(), "Downloaded PDF file does not exist"
    assert pdf_path.suffix == ".pdf", "Downloaded file is not a PDF"
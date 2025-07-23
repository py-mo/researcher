import argparse
from researcher import ArxivSearch, ArxivDownloader
from pathlib import Path

def handle_search(args):
    results = ArxivSearch(args.query, args.max_results).search()
    for idx, paper in enumerate(results, 1):
        print(f"{idx}. {paper['title']}\n   {paper['link']}\n")

def handle_download(args):
    downloader = ArxivDownloader(Path(args.output))
    success = downloader.download_pdf(args.url)
    print("Download successful" if success else "Download failed")

def main():
    parser = argparse.ArgumentParser(prog="researcher", description="Researcher CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search arXiv")
    search_parser.add_argument("query", type=str, help="Search query")
    search_parser.add_argument("--max-results", type=int, default=5, help="Maximum number of results (default: 5)")
    search_parser.set_defaults(func=handle_search)

    download_parser = subparsers.add_parser("download", help="Download a paper from URL")
    download_parser.add_argument("url", type=str, help="PDF URL")
    download_parser.add_argument("--output", type=str, default=Path("data/papers"), help="Output path(default: data/papers)")
    download_parser.set_defaults(func=handle_download)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

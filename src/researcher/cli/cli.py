import argparse
from researcher import ArxivSearch, ArxivDownloader
from researcher.pipelines import FetchPapersPipeline, EmbedPapersPipeline
from pathlib import Path

def handle_search(args):
    try:
        results = ArxivSearch(args.query, args.max_results).search()
    except Exception as e:
        print(f"{str(e)}")
    else:
        for idx, paper in enumerate(results, 1):
            print(f"{idx}. {paper['title']}\n   {paper['link']}\n")

def handle_download(args):
    try:
        downloader = ArxivDownloader(Path(args.output))
        success = downloader.download_pdf(args.url)
    except Exception as e:
        print(f"{str(e)}")
    else:
        print("✅Download successful" if success else "Download failed")

def handle_fetch_papers(args):
    try:
        pipeline = FetchPapersPipeline(args.query, args.max_results, Path(args.output))
        pipeline.run_pipeline(raise_err=True)
    except Exception as e:
        print(f"{str(e)}")
    else:
        print(f"✅Papers has been stored in {Path(args.output)} successfully!.")

def handle_embed_papers(args):
    try:
        pipeline = EmbedPapersPipeline(args.topic, Path(args.pdf_dir), Path(args.output))
        pipeline.run_pipeline(raise_err=True)
    except Exception as e:
        print(f"{str(e)}")
    else:
        print(f"✅Papers has been embedded and stored in {pipeline.index_path} successfully!.")

def main():
    parser = argparse.ArgumentParser(prog="researcher", description="Researcher CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    search_parser = subparsers.add_parser("search", help="Search arXiv")
    search_parser.add_argument("query", type=str, help="Search query")
    search_parser.add_argument("--max-results", type=int, default=5, help="Maximum number of results (default: 5)")
    search_parser.set_defaults(func=handle_search)

    download_parser = subparsers.add_parser("download", help="Download a paper from URL")
    download_parser.add_argument("url", type=str, help="PDF URL")
    download_parser.add_argument("--output", type=str, default=Path("data/embedding"), help="Output path(default: data/papers)")
    download_parser.set_defaults(func=handle_download)

    fetch_papers_parser = subparsers.add_parser("fetch-papers", help="Fetch papers from arXiv")
    fetch_papers_parser.add_argument("query", type=str, help="Search query")
    fetch_papers_parser.add_argument("--max-results", type=int, default=5, help="Maximum number of results (default: 5)")
    fetch_papers_parser.add_argument("--output", type=str, default="None", help="Output path(default: data/papers)")
    fetch_papers_parser.set_defaults(func=handle_fetch_papers)

    embed_papers_parser = subparsers.add_parser("embed-papers", help="Embed papers in directory")
    embed_papers_parser.add_argument("topic", type=str, help="Topic")
    embed_papers_parser.add_argument("pdf_dir", type=str, help="Pdfs path")
    embed_papers_parser.add_argument("--output", type=str, default="None", help="Output path(default: data/embedding)")
    embed_papers_parser.set_defaults(func=handle_embed_papers)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()

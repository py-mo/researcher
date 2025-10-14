import httpx
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Optional
from core import SearchResult, SearchResults, BasicSearchTool


class ArxivSearcher(BasicSearchTool):
    """
    Arxiv Searcher
    """


    BASE_URL = "https://export.arxiv.org/api/query"

    async def search(self, query: str, max_results: int = 5) -> SearchResults:
        """
        Perform an asynchronous search query against the arXiv API and return structured SearchResults.
        """
        params = {
            "search_query": f"all:{query}",
            "start": 0,
            "max_results": max_results,
        }

        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(self.BASE_URL, params=params)
            response.raise_for_status()

        parsed_results = await self.parse_results(response.text)
        return SearchResults(
            query=query,
            total_results=len(parsed_results),
            results=parsed_results
        )


    @staticmethod
    async def parse_results(xml_response: str) -> List[SearchResult]:
        """
        Parse the XML response from arXiv into a list of SearchResult objects.
        """
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        root = ET.fromstring(xml_response)
        results: List[SearchResult] = []

        for entry in root.findall("atom:entry", ns):
            title = (entry.find("atom:title", ns).text or "").strip()
            summary = (entry.find("atom:summary", ns).text or "").strip()

            published_date: Optional[datetime.date] = None
            published_text = entry.find("atom:published", ns)
            if published_text is not None and published_text.text:
                try:
                    published_date = datetime.fromisoformat(
                        published_text.text.replace("Z", "+00:00")
                    ).date()
                except ValueError:
                    pass

            authors = [
                a.find("atom:name", ns).text
                for a in entry.findall("atom:author", ns)
                if a.find("atom:name", ns) is not None
            ]
            link = (entry.find("atom:id", ns).text or "").strip()

            results.append(SearchResult(
                title=title,
                summary=summary,
                published=published_date,
                authors=authors,
                link=link,
            ))

        return results


if __name__ == "__main__":
    import asyncio

    async def main():
        searcher = ArxivSearcher()
        results = await searcher.search("transformer neural networks", max_results=3)
        print(results.model_dump_json(indent=2))

    asyncio.run(main())

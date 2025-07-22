import requests
import xml.etree.ElementTree as ET


class ArxivSearch:
    BASE_URL = "https://export.arxiv.org/api/query"

    def __init__(self, query: str, max_results: int = 5):
        self.query = query
        self.max_results = max_results

    def search(self):
        params = {
            "search_query": f"all:{self.query}",
            "start": 0,
            "max_results": self.max_results,
        }
        response = requests.get(self.BASE_URL, params=params)
        if response.status_code != 200:
            raise Exception(f"Arxiv API Error: {response.status_code}")

        return self.parse_results(response.text)

    @staticmethod
    def parse_results(xml_response: str):
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        root = ET.fromstring(xml_response)
        entries = []

        for entry in root.findall("atom:entry", ns):
            title = entry.find("atom:title", ns).text.strip()
            summary = entry.find("atom:summary", ns).text.strip()
            published = entry.find("atom:published", ns).text
            authors = [author.find("atom:name", ns).text for author in entry.findall("atom:author", ns)]
            link = entry.find("atom:id", ns).text

            entries.append({
                "title": title,
                "summary": summary,
                "published": published,
                "authors": authors,
                "link": link,
            })

        return entries

if __name__ == "__main__":
    searcher = ArxivSearch("Backpropagation", max_results=3)
    results = searcher.search()

    for idx, paper in enumerate(results, 1):
        print(f"{idx}. {paper['title']}\n   {paper['link']}\n")

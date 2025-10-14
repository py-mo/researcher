from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl
from datetime import date


class SearchResult(BaseModel):
    """
    Schema representing a single search result item.
    """
    title: str = Field(..., description="Title of the result (e.g., paper, article, blog)")
    summary: str = Field(..., description="Concise summary or abstract of the result")
    published: Optional[date] = Field(None, description="Publication date of the result")
    authors: Optional[List[str]] = Field(default_factory=list, description="List of authors or contributors")
    link: HttpUrl = Field(..., description="Direct link to the full content or source")


class SearchResults(BaseModel):
    """
    Schema representing a collection of search results.
    """
    query: str = Field(..., description="Original user query that produced these results")
    total_results: Optional[int] = Field(None, description="Total number of results found")
    results: List[SearchResult] = Field(..., description="List of search results")


if __name__ == "__main__":
    example_results = SearchResults(
        query="Reinforcement learning",
        total_results=1,
        results=[
            SearchResult(
                title="Policy Gradient Methods",
                summary="Overview of policy gradient techniques",
                published=date(2023, 11, 15),
                authors=["Jane Doe", "John Doe"],
                link="https://example.com/policy-gradient"
            ),
        ]
    )

    print(example_results.model_dump_json(indent=2))

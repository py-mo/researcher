from typing import Optional, List
from pathlib import Path
from researcher.pipelines import RetrieverPipeline
from researcher import ( NomicEmbedder, LLMInference
                        , FolderManager, PDFTextExtractor
                    )

class RAGOrchestrator:
    def __init__(self, embedder: NomicEmbedder, retriever: RetrieverPipeline
                 , llm: LLMInference, fm: FolderManager):
        self.embedder = embedder
        self.retriever = retriever
        self.llm = llm
        self.fm = fm

    def run(self, query: str, system_prompt: Optional[str] = None,
            options: Optional[dict] = None, k: Optional[int] = 5) -> str:
        papers_ids: List[str] = self.retriever.run_pipeline(query=query, k_neighbors=k)

        docs:List[str] = []

        for paper_id in papers_ids:
            paper_path = self.fm.get_paper_path(paper_id=paper_id)
            te = PDFTextExtractor(paper_path)
            text = te.extract_text()
            docs.append(text)

        context = "\n\n".join(docs)
        prompt = f"Use the following context to answer the question:\n\n{context}\n\nQuestion: {query}\nAnswer:"
        return self.llm.ask(prompt=prompt, system_prompt=system_prompt, options=options)
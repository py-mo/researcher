from typing import Optional, List
from researcher.pipelines import RetrieverPipeline
from researcher import ( Embedder, LLMInference
                        , FolderManager
                    )

class RAGOrchestrator:
    def __init__(self, embedder: Embedder, retriever: RetrieverPipeline
                 , llm: LLMInference, fm: FolderManager):
        self.embedder = embedder
        self.retriever = retriever
        self.llm = llm
        self.fm = fm

    def run(self, query: str, system_prompt: Optional[str] = None,
            options: Optional[dict] = None, k: Optional[int] = 5) -> str:
        chunks: List[dict] = self.retriever.run_pipeline(query=query, k_neighbors=k)

        context = ""
        for chunk in chunks:
            context += "\n\n".join(chunk["chunk"])
        prompt = f"Use the following context to answer the question:\n\n{context}\n\nQuestion: {query}\nAnswer:"
        return self.llm.ask(prompt=prompt, system_prompt=system_prompt, options=options)
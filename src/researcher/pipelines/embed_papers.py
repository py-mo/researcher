from researcher import PDFTextExtractor, NomicEmbedder, simple_chunk
from pathlib import Path


class EmbedPaperPipeline:
    def __init__(self, topic: str, pdf_dir: Path, index_path: Path = None):
        self.topic = topic
        self.pdf_dir = pdf_dir
        self.embedder = NomicEmbedder()
        self.chunker = simple_chunk
        self.index_path = index_path

    def run_pipeline(self):
        pdf_files = list(self.pdf_dir.glob("*.pdf"))

        for pdf in pdf_files:
            text = PDFTextExtractor(pdf).extract_text()

            if self.index_path:
                self.embedder.embed_and_store(pdf, self.chunker(text)[0], self.index_path)
            else:
                self.embedder.embed_and_store(pdf, self.chunker(text), Path(f"data/embedding/{self.topic}"))
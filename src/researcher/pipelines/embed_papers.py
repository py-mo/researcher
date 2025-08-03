from researcher import PDFTextExtractor, NomicEmbedder, simple_chunk
from pathlib import Path


class EmbedPapersPipeline:
    def __init__(self, topic: str, pdf_dir: Path, index_path: Path = None):
        self.topic = topic
        self.pdf_dir = pdf_dir
        self.embedder = NomicEmbedder()
        self.chunker = simple_chunk
        if (index_path != None) and (str(index_path) != "None"):
            self.index_path = index_path
        else:
            self.index_path = Path(f"data/embedding/{self.topic}")

    def run_pipeline(self, raise_err: bool = False):
        try:
            pdf_files = list(self.pdf_dir.glob("*.pdf"))
        except Exception as e:
            if raise_err:
                raise e
            print(f"Fail to read files: {str(e)}"); return;

        for pdf in pdf_files:
            try:
                text = PDFTextExtractor(pdf).extract_text()
            except Exception as e:
                if raise_err:
                    raise e
                print(f"Fail to extract text from {pdf}: {str(e)}"); continue;
            
            paper_id: str = str(pdf)[(len(str(self.pdf_dir)) + 1):-4]
            try:
                self.embedder.embed_and_store(paper_id, self.chunker(text)[0], self.index_path)
            except Exception as e:
                if raise_err:
                    raise e
                print(f"Fail to embed {pdf}: {str(e)}"); continue;
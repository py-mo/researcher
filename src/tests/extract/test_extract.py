import pytest
from pathlib import Path
from researcher import PDFTextExtractor

def test_pdf_extraction():
    pdf_path = Path("data/papers/1706.03762.pdf")

    extractor = PDFTextExtractor(pdf_path)
    extracted_text = extractor.extract_text()

    assert extracted_text[:8] == "Provided"
    assert extracted_text[-9:] == "tasks.\n15"

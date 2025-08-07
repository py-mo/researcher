import pytest
from pathlib import Path
from researcher import PDFTextExtractor
from pypdf import PdfWriter


def create_minimal_pdf(path: Path):
    writer = PdfWriter()
    writer.add_blank_page(width=595, height=842)
    with open(path, "wb") as f:
        writer.write(f)

def test_pdf_extraction(tmp_path):
    pdf_file = tmp_path / "test.pdf"
    create_minimal_pdf(pdf_file)

    extractor = PDFTextExtractor(pdf_file)
    extracted_text = extractor.extract_text()

    assert "Nothing Found" in extracted_text
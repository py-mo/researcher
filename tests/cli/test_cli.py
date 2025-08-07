import pytest
import subprocess
import sys
from pathlib import Path

def create_minimal_pdf(path: Path):
    pdf_bytes = b"""%PDF-1.4
    1 0 obj
    << /Type /Catalog /Pages 2 0 R >>
    endobj
    2 0 obj
    << /Type /Pages /Kids [3 0 R] /Count 1 >>
    endobj
    3 0 obj
    << /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792]
       /Contents 4 0 R /Resources << >> >>
    endobj
    4 0 obj
    << /Length 44 >>
    stream
    BT /F1 24 Tf 100 700 Td (Hello World) Tj ET
    endstream
    endobj
    xref
    0 5
    0000000000 65535 f 
    0000000010 00000 n 
    0000000060 00000 n 
    0000000117 00000 n 
    0000000222 00000 n 
    trailer
    << /Root 1 0 R /Size 5 >>
    startxref
    323
    %%EOF"""
    with open(path, "wb") as f:
        f.write(pdf_bytes)

CLI_PATH = Path("src/researcher/cli/cli.py")

def test_search_cli():
    result = subprocess.run(
        [sys.executable, str(CLI_PATH), "search", "graph neural networks"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "arxiv.org" in result.stdout.lower()

def test_download_cli(tmp_path):
    url = "https://arxiv.org/abs/2501.12948"
    result = subprocess.run(
        [sys.executable, str(CLI_PATH), "download", url],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "successful" in result.stdout.lower()

def test_fetch_cli():
    result = subprocess.run(
        [sys.executable, str(CLI_PATH), "fetch-papers", "deep learning"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "successfully!." in result.stdout.lower()

def test_embed_cli(tmp_path):
    pdf_file = tmp_path / "test.pdf"
    create_minimal_pdf(pdf_file)

    result = subprocess.run(
        [sys.executable, str(CLI_PATH), "embed-papers", "deep learning", f"{pdf_file}"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0
    assert "successfully!." in result.stdout.lower()

import pytest
import subprocess
import sys
from pathlib import Path

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

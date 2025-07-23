import pytest
from pathlib import Path
from researcher.storage.folder_manager import FolderManager


def test_folder_manager_creates_papers_dir(tmp_path: Path):
    fm = FolderManager(base_dir=tmp_path)

    papers_path = tmp_path / "papers"
    assert papers_path.exists() and papers_path.is_dir(), "Papers folder should be created"


def test_get_paper_path_returns_correct_path(tmp_path: Path):
    fm = FolderManager(base_dir=tmp_path)

    paper_id = "1234.5678"
    expected_path = tmp_path / "papers" / f"{paper_id}.pdf"
    actual_path = fm.get_paper_path(paper_id)

    assert actual_path == expected_path, "get_paper_path should return correct PDF path"
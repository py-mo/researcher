import pytest
import tempfile
from pathlib import Path
from researcher import EmbeddingSearcher


@pytest.fixture
def sample_data():
    return [
        ("doc1", [[1.0, 0.0, 0.0]]),
        ("doc2", [[0.0, 1.0, 0.0]]),
        ("doc3", [[0.0, 0.0, 1.0]]),
    ]


def test_build_and_search(sample_data):
    dim = 3
    with tempfile.TemporaryDirectory() as tmpdir:
        index_path = Path(tmpdir) / "test_index.ann"
        mapping_path = Path(tmpdir) / "test_mapping.json"

        searcher = EmbeddingSearcher(dim, index_path, mapping_path)
        searcher.build(sample_data)

        searcher = EmbeddingSearcher(dim, index_path, mapping_path)
        searcher.load()

        query_vector = [1.0, 0.1, 0.0]
        results = searcher.search(query_vector, k=1)

        assert isinstance(results, list)
        assert results[0] == "doc1"
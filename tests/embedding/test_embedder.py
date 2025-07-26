import pytest
from unittest.mock import patch, MagicMock
import json
from researcher import NomicEmbedder

@pytest.fixture
def embedder():
    return NomicEmbedder()

def test_embed_success(embedder):
    texts = ["hello", "world"]
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"embedding": [0.1, 0.2]}, {"embedding": [0.3, 0.4]}]}

    with patch("requests.post", return_value=mock_response):
        embeddings = embedder.embed(texts)
        assert embeddings == [[0.1, 0.2], [0.3, 0.4]]

def test_embed_invalid_input(embedder):
    with pytest.raises(ValueError):
        embedder.embed(["valid", 42])

def test_embed_failure(embedder):
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"

    with patch("requests.post", return_value=mock_response):
        with pytest.raises(RuntimeError, match="Embedding failed: Internal Server Error"):
            embedder.embed(["sample"])

def test_embed_and_store(tmp_path, embedder):
    chunks = ["chunk1", "chunk2"]
    paper_id = "paper123"
    out_dir = tmp_path

    mock_embeddings = [[0.1, 0.2], [0.3, 0.4]]
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": [{"embedding": e} for e in mock_embeddings]}

    with patch("requests.post", return_value=mock_response):
        embedder.embed_and_store(paper_id, chunks, out_dir)

        file_path = out_dir / f"{paper_id}.json"
        assert file_path.exists()

        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            assert data == [
                {"text": "chunk1", "embedding": [0.1, 0.2]},
                {"text": "chunk2", "embedding": [0.3, 0.4]}
            ]
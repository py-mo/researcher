import pytest
from unittest.mock import patch, MagicMock
import json
from researcher.embedding.embedder_ollama import OllamaEmbedder

@pytest.fixture
def embedder():
    return OllamaEmbedder()

def test_embed_success(embedder):
    texts = ["Hello, world!"]
    embeddings = embedder.embed(texts)
    assert embeddings[0][:5] == [0.36005842685699463, -0.015602553263306618, -3.588914632797241, -0.28581148386001587, -0.40117260813713074]
    texts = ["AAAAAAAA"]
    embeddings = embedder.embed(texts)
    assert embeddings[0][:5] != [0.36005842685699463, -0.015602553263306618, -3.588914632797241, -0.28581148386001587, -0.40117260813713074]


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

    embedder.embed_and_store(paper_id, chunks, out_dir)

    file_path = out_dir / f"{paper_id}.json"
    assert file_path.exists()

    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
        assert data[0]["embedding"][0][:3] == [-0.33635562658309937, -0.17253240942955017, -2.989074230194092]
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),  
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.0.1] - 2025-08-24

### Added

- Initial pipeline for paper retrieval and LLM-powered Q&A.
- **Embedder** module to embed and store paper vectors (using Annoy for similarity search).
- **Retriever** (`RetrieverPipeline`) to fetch top-k relevant papers from stored embeddings.
- **LLM Inference**:  
  - Default support with [Hugging Face Transformers](https://huggingface.co/docs/transformers/index).  
  - Alternative support via [Ollama](https://ollama.com/) and LangChain integration.  
  - Users are encouraged to use Transformers as the primary inference option.
- **UI**: Simple frontend to query the system and display results.
- Version tagging and release process initialized (`v0.0.1`).

### Notes

- This is the first tagged release of the project.  
- The pipeline is functional but minimal — future versions will focus on caching, reranking, and config flexibility.

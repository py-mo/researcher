import streamlit as st
from config import get_query_dirs
from researcher.pipelines.fetch_papers import FetchPapersPipeline
from researcher.pipelines.embed_papers import EmbedPapersPipeline
from researcher.pipelines.retriever import RetrieverPipeline
from researcher.rag.rag_orchestrator import RAGOrchestrator

st.title("📚 Researcher RAG v0.0.1")

query = st.text_input("Enter your research question:")

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a query.")
    else:
        st.info("Searching and downloading papers...")
        
        query_dirs = get_query_dirs(query)
        papers_dir = query_dirs["papers"]
        metadata_dir = query_dirs["metadata"]
        embedding_dir = query_dirs["embedding"]
        
        fetch_pipeline = FetchPapersPipeline(
            query=query,
            max_results=5,
            output_path=papers_dir,
            metadata_path=metadata_dir
        )
        fetch_pipeline.run_pipeline()

        st.subheader("🔍 Retrieved Papers")
        paper_files = list(papers_dir.glob("*.pdf"))
        if not paper_files:
            st.write("No papers found.")
        else:
            for paper_file in paper_files:
                metadata_file = metadata_dir / f"{paper_file.stem}.json"
                if metadata_file.exists():
                    import json
                    with open(metadata_file) as f:
                        metadata = json.load(f)
                        st.write(f"- {metadata.get('title', paper_file.name)}")
                else:
                    st.write(f"- {paper_file.name}")

        st.info("Embedding papers...")
        from researcher.embedding.embedder_transformers import STEmbedder
        
        embed_pipeline = EmbedPapersPipeline(
            topic=query,
            embedder=STEmbedder(),
            pdf_dir=papers_dir,
            index_path=embedding_dir,
            metadata_dir=metadata_dir
        )
        
        try:
            embed_pipeline.run_pipeline()
            st.success(f"Papers embedded successfully under {embedding_dir}")
        except Exception as e:
            st.error(f"Error embedding papers: {str(e)}")

        st.info("Retrieving context and generating answer...")
        
        embedder = STEmbedder()
        try:
            embedded_files = list(embedding_dir.glob("*.json"))
            if not embedded_files:
                st.warning("No embedded files found. Please wait for embedding to complete.")
                raise ValueError("No embedded files found.")

        except Exception as e:
            st.error(f"Error during retrieval and answer generation: {str(e)}")
        
        else:
            try:
                embedded_files = list(embedding_dir.glob("*.json"))
                embedded_files = [embedding_dir / str(p) for p in embedded_files if p.name != "annoy_mapping.json"]
                if not embedded_files:
                    st.warning("No embedded files found. Please wait for embedding to complete.")
                else:
                    retriever = RetrieverPipeline(
                        embedder=embedder,
                        embeddings_path=embedded_files,
                        index_path=embedding_dir / "annoy_index.ann",
                        mapping_path=embedding_dir / "annoy_mapping.json",
                        dim=384,
                        n_trees=10
                    )
                
                retrieved_docs = retriever.run_pipeline(query, k_neighbors=5)
                
                if retrieved_docs:
                    from researcher.rag.llm_transformers import LLMTransformers
                    from researcher import FolderManager
                    
                    fm = FolderManager()
                    llm = LLMTransformers(model="LGAI-EXAONE/EXAONE-4.0-1.2B")
                    
                    rag = RAGOrchestrator(
                        embedder=embedder,
                        retriever=retriever,
                        llm=llm,
                        fm=fm
                    )
                    
                    system_prompt = "You are a helpful research assistant. Provide accurate, well-structured answers based on the academic papers provided. Include relevant citations when possible."
                    answer = rag.run(
                        query=query,
                        system_prompt=system_prompt,
                        k=3
                    )
                    
                    st.subheader("💡 LLM Answer")
                    st.write(answer)
                else:
                    st.warning("No relevant context found in the embedded documents.")
            except Exception as e:
                st.error(f"Error during retrieval and answer generation: {str(e)}")

# 🧠 Researcher — Agentic AI for Literature Discovery

> **Version:** 0.1.0 (Agentic Mode)  
> **Goal:** Build a fully agentic pipeline for paper discovery, retrieval, embedding, and reasoning with persistent memory.

---

## 🚀 Overview

**Researcher** is an intelligent research assistant designed to search, retrieve, and reason over scientific papers autonomously.  
Version `v0.1.0` introduces a **full agentic architecture** powered by **LangGraph**, **mem0**, and **structured tool orchestration**.

The app can:

- 🔍 Search for academic papers (e.g., from ArXiv)
- 🧩 Embed, store, and retrieve papers using **Chroma**
- 🧠 Rerank and reason with LLMs
- 🗂️ Maintain short- and long-term memory via **mem0**
- ⚙️ Use **CAG (Cache-Augmented Generation)** to minimize redundant LLM calls

# 🧠 ResearcherApp

> Your personal research assistant — manage papers, take notes, track projects, and search smarter.

---

## 🛠️ Tech Stack

| Layer       | Tools |
|-------------|-------|
| Backend    | Python, LangChain |
| LLMs       | OpenAI API, Ollama |

## 🤖 Ollama Setup (Optional for Local LLMs)

To enable local LLM support using [Ollama](https://ollama.com/):

### 1️⃣ Install Ollama

Follow the official installation guide for your platform:  
[https://ollama.com/download](https://ollama.com/download)

---

### 2️⃣ Start Ollama Service

```bash
ollama serve
ollama pull phi3:mini
ollama run phi3:mini
```

| Model   | Use                   |
| ------- | --------------------- |
| llama3  | General-purpose LLM   |
| mistral | Lightweight model     |
| phi3    | Open-source assistant |

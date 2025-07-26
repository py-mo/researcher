# 🛠 Installation Guide

Follow these steps to set up **ResearcherApp** on your local machine.

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/py-mo/researcher.git
cd researcher
```
---

## 2️⃣ Setup Python Environment with uv
```bash
uv venv
source .venv/bin/activate
uv pip install -r pyproject.toml
```
---

## 3️⃣ Install and Start Ollama (Optional for Local LLMs)
Download and install ollama following installation guide [https://ollama.com/download](https://ollama.com/download)
then
```bash
ollama serve
ollama pull phi3:mini
ollama pull nomic-embed-text
ollama run phi3:mini
```
---

## 4️⃣ Install Project in Editable Mode (For Development)

To make sure Python correctly resolves the `researcher` package, install it in editable mode:

```bash
uv pip install -e .
```

---

## 5️⃣ Run the App (CLI)
```bash
python3 src/researcher/main.py
```

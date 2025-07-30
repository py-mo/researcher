# 📚 Usage Guide

This document covers how to use the `researcher` app from the command line.

---

## ✅ Prerequisites

Make sure you've installed the project in **editable mode**:

```bash
uv venv .venv
source .venv/bin/activate
uv pip install -e .
```

## 🚀 CLI Usage

Run the CLI from the project root like this:

```bash
researcher [command] [arguments]
```

or via python runner (mac and linux)

```bash
python3 src/researcher/cli/cli.py [command] [arguments]
```

(windows)

```bash
python src/researcher/cli/cli.py [command] [arguments]
```

## 🔍 Search Papers

Search arXiv for papers related to a keyword:

```bash
researcher search "graph neural networks" [--max-results N]
```

This will display a list of arXiv paper links in the terminal.

## 📥 Download Paper

Download a paper from an arXiv PDF URL:

```bash
researcher "download https://arxiv.org/2501.12948.pdf" [--output "/path/to/save/file.pdf]
```

By default, the paper will be saved to data/papers/ using the paper ID as the filename.
You can optionally specify a custom path to override the default save location.

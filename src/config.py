from pathlib import Path

# Get the project root directory (3 levels up from this file)
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
PAPERS_DIR = DATA_DIR / "papers"
METADATA_DIR = DATA_DIR / "metadata"
EMBEDDING_DIR = DATA_DIR / "embedding"

# Create directories if they don't exist
for dir_path in [PAPERS_DIR, METADATA_DIR, EMBEDDING_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

def get_query_dirs(query: str):
    """Get the directory paths for a specific query."""
    # Sanitize query for filesystem use
    safe_query = "".join(c if c.isalnum() else "_" for c in query).lower()
    
    return {
        "papers": PAPERS_DIR / safe_query,
        "metadata": METADATA_DIR / safe_query,
        "embedding": EMBEDDING_DIR / safe_query
    }

from typing import List

def simple_chunk(text: str, max_tokens: int = 256, overlap: int = 32) -> List[str]:
    words = text.split()
    length = len(words)
    chunks = []
    for i in range(0, len(words), max_tokens):
        if i + overlap + max_tokens < length:
            if i > overlap:
                chunks.append(" ".join(words[(i - overlap):i + max_tokens + overlap]))
            else:
                chunks.append(" ".join(words[i:i + max_tokens + overlap]))
        elif i >= overlap:
            chunks.append(" ".join(words[(i - overlap):i + max_tokens]))
        else:
            chunks.append(" ".join(words[i:i + max_tokens]))
    return chunks
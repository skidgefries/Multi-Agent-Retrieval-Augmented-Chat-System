# ingest/chunker.py
import re


def clean_text(text: str) -> str:
    # remove multiple spaces and normalize newlines
    text = text.replace('\r', '\n')
    text = re.sub(r"\n+", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()




def chunk_text(text: str, chunk_size=400, overlap=50):
    """Simple word-based chunking with overlap.
    chunk_size: number of words per chunk
    overlap: number of overlapping words between consecutive chunks
    """
    text = clean_text(text)
    words = text.split()
    if len(words) <= chunk_size:
        return [text]
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunk = ' '.join(words[start:end])
        chunks.append(chunk)
        if end == len(words):
            break
        start = end - overlap
    return chunks
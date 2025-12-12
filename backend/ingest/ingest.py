# ingest/ingest.py
import os
from .chunker import chunk_text
from agents.embedder import Embedder
from db.db import get_session, Base, engine
from db.models import Document, serialize_embedding
from sqlalchemy.orm import Session
from tqdm import tqdm


DOCS_FOLDER = os.getenv("DOCS_FOLDER", "docs")




def load_documents(folder=DOCS_FOLDER):
    texts = []
    for fname in os.listdir(folder):
        if fname.lower().endswith('.txt'):
            path = os.path.join(folder, fname)
            with open(path, 'r', encoding='utf-8') as f:
                texts.append((fname, f.read()))
    return texts




def run_ingest(chunk_size=400, overlap=50):
    Base.metadata.create_all(bind=engine)
    embedder = Embedder()
    session: Session = get_session()


    docs = load_documents()
    total_chunks = 0
    for fname, text in docs:
        chunks = chunk_text(text, chunk_size=chunk_size, overlap=overlap)
        embeddings = embedder.embed(chunks)
        for idx, (chunk, emb) in enumerate(zip(chunks, embeddings)):
            blob = serialize_embedding(emb)
            doc = Document(source=fname, chunk_index=idx, content=chunk, embedding=blob)
            session.add(doc)
        session.commit()
        total_chunks += len(chunks)
        print(f"Ingested {len(chunks)} chunks from {fname}")
    session.close()
    print(f"Total chunks ingested: {total_chunks}")


if __name__ == '__main__':
    run_ingest()
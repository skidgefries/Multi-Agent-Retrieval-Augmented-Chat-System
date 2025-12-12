# agents/supervisor.py
from agents.embedder import Embedder
from agents.retriever import Retriever
from agents.generator import Generator
from db.db import get_session


class Supervisor:
    def __init__(self):
        self.embedder = Embedder()
        self.retriever = Retriever()
        self.generator = Generator()
        # build index from DB
        self.retriever.build()


    def refresh_index(self):
        self.retriever.build() 


    def ingest_documents(self, texts, source_name='inline'):
        # convenience wrapper: chunk -> embed -> save
        from database.db import Base, engine
        from database.models import Document, serialize_embedding
        from database.db import get_session
        from ingest.chunker import chunk_text


        Base.metadata.create_all(bind=engine)
        session = get_session()
        chunks = []
        for i, t in enumerate(texts):
            pieces = chunk_text(t)
            for idx, p in enumerate(pieces):
                chunks.append((f"{source_name}_{i}", idx, p))
        embs = self.embedder.embed([c[2] for c in chunks])
        for (src, idx, content), emb in zip(chunks, embs):
            blob = serialize_embedding(emb)
            d = Document(source=src, chunk_index=idx, content=content, embedding=blob)
            session.add(d)
        session.commit()
        session.close()
        self.refresh_index()


    def answer_question(self, question: str, top_k=3):
        q_emb = self.embedder.embed(question)
        results = self.retriever.search(q_emb, top_k=top_k)
        answer = self.generator.generate(question, results)
        return {
            'question': question,
            'contexts': results,
            'answer': answer
        }
        


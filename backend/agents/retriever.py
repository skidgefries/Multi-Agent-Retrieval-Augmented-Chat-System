# agents/retriever.py
import faiss
import numpy as np
from db.db import get_session
from db.models import deserialize_embedding, Document


class Retriever:
    def __init__(self, dim=None):
        self.dim = dim
        self.index = None
        self.id_map = [] # list of (db_id, source, chunk_index, content)


    def build(self):
        session = get_session()
        rows = session.query(Document).all()
        session.close()
        if not rows:
            self.index = None
            self.id_map = []
            return
        embs = np.stack([deserialize_embedding(r.embedding) for r in rows])
        embs = embs.astype('float32')
        self.dim = embs.shape[1]
        faiss.normalize_L2(embs)
        self.index = faiss.IndexFlatIP(self.dim)
        self.index.add(embs)
        self.id_map = [(r.id, r.source, r.chunk_index, r.content) for r in rows]


    def search(self, q_emb, top_k=3):
        if self.index is None or self.index.ntotal == 0:
            return []
        q = q_emb.astype('float32').reshape(1, -1)
        faiss.normalize_L2(q)
        D, I = self.index.search(q, top_k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx < 0:
                continue
            db_id, source, chunk_index, content = self.id_map[idx]
            results.append({
                'id': db_id,
                'source': source,
                'chunk_index': chunk_index,
                'content': content,
                'score': float(score)
            })
        return results
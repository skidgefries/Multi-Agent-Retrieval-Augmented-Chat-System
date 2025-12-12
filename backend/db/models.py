# database/models.py
from sqlalchemy import Column, Integer, Text, LargeBinary, String
from db.db import Base
import pickle


class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=True)
    chunk_index = Column(Integer, nullable=True)
    content = Column(Text, nullable=False)
    embedding = Column(LargeBinary, nullable=False) # pickled float32


# helpers
def serialize_embedding(emb):
    return pickle.dumps(emb.astype('float32'))


def deserialize_embedding(blob):
    return pickle.loads(blob)
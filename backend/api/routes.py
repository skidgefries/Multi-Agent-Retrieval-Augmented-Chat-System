# api/routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from agents.supervisor import Supervisor


router = APIRouter()
# single supervisor instance
supervisor = Supervisor()


class IngestRequest(BaseModel):
    texts: list[str]


class ChatRequest(BaseModel):
    question: str


@router.post('/ingest')
def ingest(req: IngestRequest):
    try:
        supervisor.ingest_documents(req.texts, source_name='api')
        return {'status': 'ok', 'ingested': len(req.texts)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/chat')
def chat(req: ChatRequest):
    try:
        res = supervisor.answer_question(req.question)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
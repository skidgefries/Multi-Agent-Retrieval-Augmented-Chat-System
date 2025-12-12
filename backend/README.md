# mini_rag — Minimal RAG demo


## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Ensure Postgres is running and set `DATABASE_URL` env var, e.g.:
`export DATABASE_URL=postgresql://postgres:password@localhost:5432/mini_rag`
3. Put 5-7 long `.txt` files into `docs/`.
4. Run ingestion once: `python ingest/ingest.py`.
5. Start API: `python main.py`.
6. Ingest via API (optional) or query:
- POST `/api/chat` with `{ "question": "..." }`
- POST `/api/ingest` with `{ "texts": ["long text 1", "long text 2"] }`


## Notes
- Use small models for local demos. Replace `distilgpt2` or embedder model if GPU available.
- The FAISS index is built at startup and after ingestion. For large data, persist it to disk.
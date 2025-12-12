# main.py
from fastapi import FastAPI
from api.routes import router
from db.db import Base, engine
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title='mini_rag')
app.include_router(router, prefix='/api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event('startup')
def startup():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
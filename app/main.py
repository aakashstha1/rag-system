from fastapi import FastAPI
from app.routes.rag import router

app = FastAPI(
    title="RAGIFY API",
    version="1.0.0"
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "RAGIFY API Running"
    }
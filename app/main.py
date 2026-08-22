from fastapi import FastAPI
from app.routes.rag import router

# Create FastAPI application instance
app = FastAPI(
    title="RAG SYSTEM",
    version="1.0.0"
)

# Include all routes
app.include_router(router)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "RAGIFY API Running"
    }
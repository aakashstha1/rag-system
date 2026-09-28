import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.rag import router
from dotenv import load_dotenv

load_dotenv()

# Create FastAPI application instance
app = FastAPI(
    title="RAG SYSTEM",
    version="1.0.0"
)


# Allow the React frontend (running on a different port) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes
app.include_router(router)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "RAGIFY API Running"
    }
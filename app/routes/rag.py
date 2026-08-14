from fastapi import APIRouter, UploadFile, File
from pathlib import Path
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import create_chunks
from app.services.embedding_service import create_embeddings
from app.services.vector_store import store_chunks
from app.schemas.chat import ChatRequest
from app.services.llm_service import generate_answer
from app.services.vector_store import retrieve_documents
from pydantic import BaseModel

router = APIRouter()

# Folder where uploaded PDFs will be stored
UPLOAD_DIR = Path("uploads")

# Create the uploads folder if it doesn't exist
UPLOAD_DIR.mkdir(exist_ok=True)


# Route to upload a PDF file
@router.post("/upload")
async def upload_file(
    # Uploaded file is required
    file: UploadFile = File(...)
):
    # Create the file path
    file_path = UPLOAD_DIR / file.filename

    # Save the uploaded file to disk
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Extract text from the PDF
    text = extract_text_from_pdf(str(file_path))

    # Return an error if no text was found
    if not text.strip():
        return {
            "error": "No extractable text found"
        }

    # Split text into smaller chunks
    chunks = create_chunks(text)

    # Create embeddings for all chunks
    embeddings = create_embeddings(chunks)

    # Store chunks and embeddings in ChromaDB
    document_id = store_chunks(
        chunks,
        embeddings,
        file.filename
    )

    # Return upload information
    return {
        "document_id": document_id,
        "filename": file.filename,
        "chunks": len(chunks)
    }


# Request body model for search endpoint
class QueryRequest(BaseModel):
    question: str


# Route to search relevant chunks
@router.post("/search")
def search_documents(
    payload: QueryRequest
):
    # Retrieve similar chunks based on the question
    document = retrieve_documents(payload.question)

    return {
        "question": payload.question,
        "retrieved_chunks": document
    }


# Route to chat with uploaded documents
@router.post("/chat")
def chat(
    data: ChatRequest
):
    # Retrieve relevant chunks for the question
    retrieved = retrieve_documents(
        data.question
    )

    # Extract the retrieved documents
    documents = retrieved["documents"]

    # Combine documents into a single context
    context = "\n\n".join(
        documents
    )

    # Generate an answer using the LLM
    answer = generate_answer(
        question=data.question,
        context=context
    )

    # Extract unique source filenames
    sources = [
    {
        "filename": meta["filename"],
        "chunk_index": meta["chunk_index"]
    }
    for meta in retrieved["metadatas"]
    ]

    # Return the answer and source documents
    return {
        "question": data.question,
        "answer": answer,
        "sources": sources
    }
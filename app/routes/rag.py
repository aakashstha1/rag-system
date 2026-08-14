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

UPLOAD_DIR = Path("uploads")
# Create the directory if it doesn't exist
UPLOAD_DIR.mkdir(exist_ok=True) 


# Route to handle file uploads
@router.post("/upload")
async def upload_file(
    # ... means required parameter
    file: UploadFile = File(...)
):
    file_path = UPLOAD_DIR / file.filename
    # Open the file in write-binary mode ("wb")
    # If the file doesn't exist, it will be created
    # If it already exists, its contents will be overwritten
    with open(file_path, "wb") as buffer:
         # Read the uploaded file's contents as bytes
        # 'await' is needed because UploadFile.read() is asynchronous
        # Write the bytes to the file on disk
        buffer.write(await file.read())

    text = extract_text_from_pdf(str(file_path))

    if not text.strip():
        return {
            "error": "No extractable text found"
        }

    chunks = create_chunks(text)

    embeddings = create_embeddings(chunks)

    document_id = store_chunks(
    chunks,
    embeddings,
    file.filename
)

    return {
    "document_id": document_id,
    "filename": file.filename,
    "chunks": len(chunks)
}

# Pydantic model to validate request body
class QueryRequest(BaseModel):
    question: str

# Route to handle search queries
@router.post("/search")
def search_documents(
    payload: QueryRequest
):
    # embedding = create_embedding(
    #     payload.question
    # )

    # results = search_chunks(embedding)

    document = retrieve_documents(payload.question)


    # return results
    return {
    "question": payload.question,
    "retrieved_chunks":document
}

@router.post("/chat")
def chat(
    data: ChatRequest
):
    retrieved = retrieve_documents(
        data.question
    )

    documents = retrieved["documents"]

    context = "\n\n".join(
        documents
    )

    answer = generate_answer(
        question=data.question,
        context=context
    )

    
    sources = list({
    metadata["filename"]
    for metadata in retrieved["metadatas"]
    if metadata and "filename" in metadata
    })

    return {
        "question": data.question,
        "answer": answer,
        "sources": sources
    }
from fastapi import APIRouter, UploadFile, File
from pathlib import Path
from app.services.pdf_service import extract_text_from_pdf
from app.services.chunk_service import create_chunks
from app.services.embedding_service import create_embedding

router = APIRouter()

UPLOAD_DIR = Path("uploads")
# Create the directory if it doesn't exist
UPLOAD_DIR.mkdir(exist_ok=True) 


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

    text = extract_text_from_pdf(file_path)

    chunks = create_chunks(text)

    embedding = create_embedding(chunks[0])

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "chunks": len(chunks),
        "embedding dimension":len(embedding)
    }
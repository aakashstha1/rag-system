import chromadb
from app.services.embedding_service import create_embedding
import uuid

# Create a ChromaDB client and store data in the "chroma_db" folder
client = chromadb.PersistentClient(
    path="chroma_db"
)

# Create the collection if it doesn't exist, otherwise use the existing one
collection = client.get_or_create_collection(
    name="documents"
)

# Store text chunks and their embeddings in ChromaDB
def store_chunks(
    chunks: list[str],
    embeddings: list[list[float]],
    filename: str
) -> str:

    document_id = str(uuid.uuid4())


    ids = [
        f"{document_id}_chunk_{i}"
        for i in range(len(chunks))
    ]

    metadatas = [
    {
        "document_id": document_id,
        "filename": filename,
        "chunk_index": i
    }
    for i in range(len(chunks))
    ]

    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    return document_id
    
# Search for similar chunks
def search_chunks(
    query_embedding,
    n_results: int = 3
):
    results = collection.query(
    query_embeddings=[query_embedding],
    n_results=n_results,
    include=[
        "documents",
        "metadatas",
        "distances"
    ]
)

    return results


def retrieve_documents(
    question: str
):
    query_embedding = create_embedding(
        question
    )

    results = search_chunks(
        query_embedding
    )

    return {
    "documents": results["documents"][0],
    "metadatas": results["metadatas"][0],
    "distances": results["distances"][0]
}
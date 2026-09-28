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

    # Generate a unique ID for the uploaded document
    document_id = str(uuid.uuid4())

    # Create a unique ID for each chunk
    ids = [
        f"{document_id}_chunk_{i}"
        for i in range(len(chunks))
    ]

    # Store extra information about each chunk
    metadatas = [
        {
            "document_id": document_id,
            "filename": filename,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]

    # Save chunks, embeddings, and metadata to ChromaDB
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    # Return the document ID
    return document_id


# Search for similar chunks using a query embedding
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


# Retrieve the most relevant documents for a question
def retrieve_documents(
    question: str
):
    # Convert the question into an embedding
    query_embedding = create_embedding(
        question
    )

    # Search for similar chunks
    results = search_chunks(
        query_embedding
    )

    # Return documents, metadata, and similarity scores
    return {
        "documents": results["documents"][0],
        "metadatas": results["metadatas"][0],
        "distances": results["distances"][0]
    }


# Delete all chunks belonging to a single uploaded document
def delete_document(document_id: str):
    # Find the chunks belonging to this document before deleting, so the
    # caller knows whether anything was removed and what the file was called
    existing = collection.get(
        where={"document_id": document_id}
    )
    deleted_count = len(existing["ids"])

    filename = None
    if deleted_count > 0:
        filename = existing["metadatas"][0]["filename"]
        collection.delete(
            where={"document_id": document_id}
        )

    return {
        "deleted_count": deleted_count,
        "filename": filename
    }

    # List every uploaded document with its chunk count
def list_documents():
    # Only metadata is needed, so skip loading chunk text and embeddings
    stored = collection.get(include=["metadatas"])

    # Group chunks by document_id
    documents = {}
    for metadata in stored["metadatas"]:
        doc = documents.setdefault(
            metadata["document_id"],
            {
                "document_id": metadata["document_id"],
                "filename": metadata["filename"],
                "chunks": 0
            }
        )
        doc["chunks"] += 1

    return sorted(documents.values(), key=lambda d: d["filename"].lower())
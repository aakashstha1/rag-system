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
import chromadb
from app.services.embedding_service import create_embedding

# Create a ChromaDB client and store data in the "chroma_db" folder
client = chromadb.PersistentClient(
    path="chroma_db"
)

# Create the collection if it doesn't exist, otherwise use the existing one
collection = client.get_or_create_collection(
    name="documents"
)

# Store text chunks and their embeddings in ChromaDB
def store_chunks(chunks, embeddings):

    # List to store unique IDs for each chunk
    ids = []

    # Create an ID for every chunk
    for i in range(len(chunks)):
        ids.append(str(i))

    # Save IDs, text chunks, and embeddings to the collection
    collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings
    )

    
# Search for similar chunks
def search_chunks(
    query_embedding,
    n_results: int = 3
):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
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

    return results["documents"][0]
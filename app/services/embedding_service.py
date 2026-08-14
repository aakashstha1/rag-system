from sentence_transformers import SentenceTransformer

# The model converts meaning into a point in a 384-dimensional space.
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embeddings(chunks: list[str]) -> list[list[float]]:
    # Convert the input text into a numerical vector (embedding)
    # Convert NumPy array to a Python list
    # This makes it easier to store in JSON, databases, or vector stores
    return model.encode(chunks).tolist()

def create_embedding(text: str) -> list[float]:
    return model.encode(text).tolist()
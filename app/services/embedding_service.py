from sentence_transformers import SentenceTransformer

# The model converts meaning into a point in a 384-dimensional space.
model = SentenceTransformer('all-MiniLM-L6-v2')

def create_embedding(text: str) -> list[float]:
    # Convert the input text into a numerical vector (embedding)
    # Convert NumPy array to a Python list
    # This makes it easier to store in JSON, databases, or vector stores
    return model.encode(text).tolist()
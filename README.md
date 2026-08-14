# RAGIFY - RAG System 

A simple Retrieval-Augmented Generation (RAG) system built with FastAPI.

The application allows users to:

- Upload PDF documents
- Extract text from PDFs
- Split text into chunks
- Generate embeddings using Sentence Transformers
- Store embeddings in ChromaDB
- Retrieve relevant chunks based on user questions
- Generate answers using Groq LLM

---

## Tech Stack

- Python
- FastAPI
- ChromaDB
- Sentence Transformers
- Groq
- PyPDF
- LangChain Text Splitters

---

## Project Structure

```text
rag-system/
│
├── app/
│   ├── routes/
│   │   └── rag.py
│   │
│   ├── schemas/
│   │   └── chat.py
│   │
│   ├── services/
│   │   ├── pdf_service.py
│   │   ├── chunk_service.py
│   │   ├── embedding_service.py
│   │   ├── vector_store.py
│   │   └── llm_service.py
│   │
│   └── main.py
│
├── uploads/
├── chroma_db/
├── run.py
├── requirements.txt
└── README.md
```

---

## Features

### Upload PDF

Upload a PDF document to the system.

- Saves file locally
- Extracts text from PDF
- Creates chunks
- Generates embeddings
- Stores data in ChromaDB

### Search Documents

Search relevant document chunks using semantic search.

- Converts question into embedding
- Searches ChromaDB
- Returns most relevant chunks
- Returns chunk metadata
- Returns similarity scores (distances)
- Supports retrieval debugging

### Chat with Documents

Ask questions about uploaded documents.

- Retrieves relevant chunks
- Sends context and question to Groq
- Generates final answer
- Uses retrieved context from ChromaDB
- Returns source citations
- Supports multiple uploaded documents

---

## Installation

### Clone Repository

```bash
git clone https://github.com/aakashstha1/rag-system.git
cd rag-system
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Mac/Linux:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root directory.

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Run the Application

```bash
python run.py
```

or

```bash
uvicorn app.main:app --reload
```

Server runs at:

```text
http://127.0.0.1:8000
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## API Documentation

FastAPI automatically generates interactive API documentation.

### Swagger UI

Open:

```text
http://127.0.0.1:8000/docs
```

You can:

- View all available endpoints
- Test API requests directly from the browser
- Upload PDF files
- Send chat queries
- Inspect request and response schemas

### ReDoc

Open:

```text
http://127.0.0.1:8000/redoc
```

This provides an alternative API documentation interface.

---

## API Endpoints

### Upload PDF

```http
POST /upload
```

Upload a PDF document.

---

### Search Documents

```http
POST /search
```

Request:

```json
{
  "question": "What is FastAPI?"
}
```

---

### Chat

```http
POST /chat
```

Request:

```json
{
  "question": "What is FastAPI?"
}
```

Response:

```json
{
  "question": "What is FastAPI?",
  "answer": "FastAPI is a modern Python framework...",
  "sources": [
    {
      "filename": "fastapi.pdf",
      "chunk_index": 2
    }
  ]
}
```
---

## Metadata Stored

Each chunk is stored with:

```json
{
  "document_id": "uuid",
  "filename": "document.pdf",
  "chunk_index": 0
}

```
---

## Architecture

```text
PDF Upload
    ↓
PDF Extraction (PyPDF)
    ↓
Chunking (LangChain)
    ↓
Embeddings (Sentence Transformers)
    ↓
ChromaDB Vector Store
    ↓
Semantic Retrieval
    ↓
Groq LLM
    ↓
Answer + Source Citations
```

---

## Future Improvements

- Conversation memory
- Frontend interface
- Docker deployment
- Hybrid search (keyword + vector search)
- Reranking for improved retrieval

---

## Author

Aakash Shrestha

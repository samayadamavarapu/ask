# 🧘 Ask Me Anything About Yoga

A production-ready RAG-based AI micro-application that answers questions about Yoga and Wellness using a structured knowledge base.

## 🚀 Features

- **RAG Pipeline**:
  - **Ingestion**: Supports JSON, TXT, PDF, MD.
  - **Chunking**: Configurable semantic splitting.
  - **Embeddings**: Uses `sentence-transformers/all-MiniLM-L6-v2` (Local) and ChromaDB.
  - **Retrieval**: Semantic similarity search.
  - **Generation**: LLM-based answers grounded in retrieved context (OpenAI compatible).
- **Safety First**:
  - Detects medical/sensitive queries locally.
  - Blocks dangerous queries.
  - Softens sensitive responses with disclaimers.
  - Flags: `SAFE`, `SENSITIVE`, `BLOCKED`.
- **Production Logging**:
  - MongoDB logging for every interaction (Query, Response, Safety Flag, Context).
- **Architecture**:
  - Modular `app/` structure (API, Core, Services, DB).
  - FastAPI Backend.
  - Async Database Operations.
- **Frontend**:
  - Simple, clean HTML/JS chat interface.

## 🏃 Quick Start / Execution Guide

Follow these steps to get the app running in minutes:

1.  **Start MongoDB**: Ensure your MongoDB server is running locally (usually on port 27017).
2.  **Navigate to Backend**: Open your terminal and go to the `backend` folder:
    ```bash
    cd yoga/backend
    ```
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Ingest Data**: Load the yoga knowledge base into the vector store:
    ```bash
    python ingest_data.py
    ```
5.  **Run the Server**:
    ```bash
    uvicorn app.main:app --reload
    ```

6.  **Open the App**: Go to **http://localhost:8000** in your browser.

## 🛠️ Detailed Setup & Installation

### Prerequisites
- Python 3.8+
- MongoDB (Running locally or cloud URI)
- OpenAI API Key (Optional, for generation)

### 1. Clone & Install
```bash
git clone <repo>
cd yoga/backend
pip install -r requirements.txt
```

### 2. Environment Configuration
Copy `.env.example` to `.env` (or just use the provided `.env`) in the `backend` folder and update values:
```bash
MONGODB_URL=mongodb://localhost:27017
OPENAI_API_KEY=sk-...
```

### 3. Ingest Knowledge Base
Load the sample data (or your own files in `data/knowledge_base`):
```bash
python ingest_data.py
```
This processes files, generates embeddings, and stores them in ChromaDB (`backend/data/chroma_db`).

### 4. Run the Application
```bash
uvicorn app.main:app --reload
```
Visit `http://localhost:8000` to use the Chat UI.

### 5. API Documentation
Visit `http://localhost:8000/docs` for Swagger UI.

## ✅ Track B Compliance

This micro-app meets the following Track B requirements:

1.  **RAG Design**: Complete pipeline with Chunking -> Embedding -> Vector Search -> Generation.
2.  **Safety Logic**:
    -   **Medical/Pregnancy Detection**: Keywords like "pregnancy", "illness", "pain" trigger a `SENSITIVE` or `UNSAFE` flag.
    -   **Structured Warnings**: UI displays a red warning block for unsafe queries.
    -   **Refusal**: Blocks queries that are harmful or non-yoga related.
3.  **MongoDB Logging**:
    -   Logs every interaction with `is_unsafe` flag, query, response, and retrieved chunks.
4.  **UI Features**:
    -   **Sources Display**: Lists the titles of knowledge base articles used.
    -   **Feedback**: Thumbs Up/Down buttons for user feedback.
    -   **Visuals**: Yoga-themed background, glassmorphism design.

## 📝 Prompts List

The application uses the following system prompts (located in `app/services/generation.py`):

**System Prompt:**
> "You are a helpful and peaceful Yoga Assistant. Use the provided context to answer the user's question. If the context does not contain the answer, say you don't know but offer general wellness advice.
> 
> Safety First: If the question is about medical issues, pregnancy, or acute pain, advise the user to consult a doctor. Do not give medical advice.
> 
> Tone: Calm, encouraging, and respectful (Namaste)."

## 🏗️ Design Decisions

- **Framework**: **FastAPI** chosen for speed, async support, and auto-generated docs.
- **Vector Store**: **ChromaDB** for easy local persistence without complex infrastructure setup.
- **Embeddings**: **SentenceTransformers** (Local) to reduce API costs and dependency.
- **Frontend**: **Vanilla HTML/JS** served by FastAPI for a lightweight, single-deployable unit.

## 📂 Project Structure
```
yoga/
├── backend/
│   ├── app/
│   │   ├── api/          # Routes & Schemas
│   │   ├── core/         # Config & Settings
│   │   ├── db/           # Database Connection
│   │   ├── services/     # Business Logic (RAG, Safety)
│   │   └── main.py       # App Entrypoint
│   ├── ingest_data.py    # Ingestion Script
│   └── requirements.txt
├── frontend/             # HTML/CSS/JS Assets
│   └── index.html
└── data/                 # Knowledge Base JSONs
```

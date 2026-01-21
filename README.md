# Cybersecurity Knowledge Assistant - Simple RAG Project

A beginner-friendly Retrieval-Augmented Generation (RAG) system that answers cybersecurity questions using only the provided documents.

## What This Project Does

1. Loads cybersecurity documents from the `/backend/docs` folder
2. Breaks them into smaller chunks
3. Creates embeddings (numerical representations) of the text
4. Stores them in FAISS (a vector database)
5. When you ask a question:
   - Converts your question to an embedding
   - Finds similar chunks from documents
   - Sends them to LLaMA 3 with your question
   - Gets an answer based ONLY on those documents
6. Shows you the answer and which documents it came from

## Folder Structure

```
project/
├── backend/                  # Python backend
│   ├── docs/                # Cybersecurity documents (7 files)
│   │   ├── phishing.txt
│   │   ├── malware.txt
│   │   ├── passwords.txt
│   │   ├── firewalls.txt
│   │   ├── social_engineering.txt
│   │   ├── encryption.txt
│   │   └── vpn.txt
│   ├── main.py              # FastAPI server with RAG logic
│   └── requirements.txt     # Python dependencies
└── src/                     # React frontend
    └── App.tsx              # Simple UI
```

## Prerequisites

Before starting, you need:

1. **Python 3.9 or higher**
   - Check: `python --version` or `python3 --version`

2. **Node.js and npm**
   - Check: `node --version` and `npm --version`

3. **Ollama with LLaMA 3**
   - Install Ollama from: https://ollama.ai
   - After installing, run: `ollama pull llama3`

## Step-by-Step Setup

### Step 1: Install Backend Dependencies

Open a terminal and navigate to the backend folder:

```bash
cd backend
```

Create a virtual environment (optional but recommended):

```bash
python -m venv venv
```

Activate the virtual environment:
- On Mac/Linux: `source venv/bin/activate`
- On Windows: `venv\Scripts\activate`

Install Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- FastAPI (web framework)
- LangChain (RAG framework)
- sentence-transformers (for embeddings)
- FAISS (vector database)
- Ollama (to connect to LLaMA)

### Step 2: Start the Backend Server

Make sure you're in the `backend` folder, then run:

```bash
python main.py
```

You should see:
```
Loading documents...
Loaded 7 documents
Splitting documents into chunks...
Created XX chunks
Creating embeddings and vector store...
RAG system ready!
```

The server is now running on `http://localhost:8000`

**Keep this terminal open!**

### Step 3: Install Frontend Dependencies

Open a NEW terminal (keep the backend running in the first one).

Navigate to the project root:

```bash
cd ..
```

Install Node packages:

```bash
npm install
```

### Step 4: Start the Frontend

In the same terminal, run:

```bash
npm run dev
```

The frontend will start on `http://localhost:5173`

### Step 5: Use the Application

1. Open your browser and go to `http://localhost:5173`
2. You'll see a simple page with:
   - Input box for questions
   - Submit button
   - Space for answers and sources

3. Try asking questions like:
   - "What is phishing?"
   - "How do I create strong passwords?"
   - "What is a VPN?"
   - "What is malware?"

4. The system will:
   - Show the answer from the documents
   - List which documents were used

5. Try asking something NOT in the documents:
   - "What is quantum computing?"
   - You should get: "I don't know based on the provided documents."

## How It Works (Simple Explanation)

### 1. Loading Documents
The system reads all `.txt` files from the `docs` folder.

### 2. Splitting Text
Long documents are split into chunks of ~500 characters. This makes searching easier.

### 3. Creating Embeddings
Each chunk is converted to numbers (embeddings) using a model called `all-MiniLM-L6-v2`. Similar text has similar numbers.

### 4. Storing in FAISS
FAISS stores these embeddings and can quickly find similar ones.

### 5. Answering Questions
When you ask a question:
1. Your question is converted to an embedding
2. FAISS finds the 3 most similar chunks
3. These chunks are sent to LLaMA 3 as "context"
4. LLaMA generates an answer using ONLY that context

### 6. The Prompt
The prompt tells LLaMA:
```
"Answer only from the given context.
If the answer is not in the context, say 'I don't know based on the provided documents.'"
```

This prevents LLaMA from using its training data.

## API Documentation

### Endpoint: POST /ask

**Request:**
```json
{
  "question": "What is phishing?"
}
```

**Response:**
```json
{
  "answer": "Phishing is a type of cyber attack where...",
  "sources": ["phishing.txt", "social_engineering.txt"]
}
```

## Adding Your Own Documents

To add more documents:

1. Create a new `.txt` file in `backend/docs/`
2. Write content about any cybersecurity topic
3. Restart the backend server
4. The new document will be included automatically

## Troubleshooting

### Backend won't start
- Make sure Python packages are installed: `pip install -r requirements.txt`
- Check if port 8000 is available
- Verify Ollama is running: `ollama list`

### "Error: Could not connect to backend"
- Make sure the backend server is running on port 8000
- Check the backend terminal for errors

### Ollama errors
- Make sure Ollama is installed
- Pull LLaMA 3: `ollama pull llama3`
- Check if Ollama is running: `ollama list`

### Slow responses
- This is normal! LLaMA 3 takes time to generate answers
- First time is slower because it loads the model

## Project Files Explained

### backend/main.py
- Sets up FastAPI server
- Loads documents and creates chunks
- Creates embeddings with sentence-transformers
- Stores in FAISS vector database
- Handles /ask endpoint
- Uses LangChain to connect everything

### backend/docs/*.txt
- 7 cybersecurity documents
- Covers: phishing, malware, passwords, firewalls, social engineering, encryption, VPN

### src/App.tsx
- Simple React component
- Input box for questions
- Displays answers and sources
- Calls backend API

## Key Technologies

1. **FastAPI** - Python web framework (simple and fast)
2. **LangChain** - Framework for building RAG applications
3. **sentence-transformers** - Creates embeddings from text
4. **FAISS** - Vector database (stores and searches embeddings)
5. **Ollama** - Runs LLaMA 3 locally
6. **React + Vite** - Simple frontend

## Learning Resources

- **RAG**: Combines retrieval (finding documents) + generation (LLM answers)
- **Embeddings**: Converting text to numbers that capture meaning
- **Vector Store**: Database optimized for finding similar embeddings
- **LLM**: Large Language Model (LLaMA 3) generates natural language

## Next Steps (If You Want to Learn More)

1. Add more documents
2. Try different chunk sizes in `main.py`
3. Change the number of retrieved chunks (k=3)
4. Experiment with different prompts
5. Try other embedding models
6. Add conversation history

## License

This is a learning project. Use it however you want!

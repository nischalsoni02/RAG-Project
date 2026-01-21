# RAG-project-Nischal_Soni

A Retrieval-Augmented Generation (RAG) system that answers cybersecurity questions using only the provided documents.

Working Demo Images:
Image1:https://drive.google.com/file/d/1Zb0jhA2xyB3KXnoAtCLvyI9otiKcReud/view?usp=drivesdk

Image2:https://drive.google.com/file/d/17CcIxmC0bmaqQn6LfeDyjzKItiDE8S0U/view?usp=drivesdk

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
├── backend/                  
│   ├── docs/                
│   │   ├── phishing.txt
│   │   ├── malware.txt
│   │   ├── passwords.txt
│   │   ├── firewalls.txt
│   │   ├── social_engineering.txt
│   │   ├── encryption.txt
│   │   └── vpn.txt
│   ├── main.py              
│   └── requirements.txt     
└── src/                     
    └── App.tsx              
```

## Prerequisites

1. **Python 3.9 or higher**
2. **Node.js and npm**
3. **Ollama with LLaMA 3**
   - Install Ollama from: https://ollama.ai
   - After installing, run: `ollama pull llama3`

## Step-by-Step Setup

### Step 1: Install Backend Dependencies
```bash
cd backend
```
Create a virtual environment
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

Open a NEW terminal
Install Node packages:

```bash
npm install
```

### Step 4: Start the Frontend

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
   - "What is an apple?"
   - You will get: "I don't know based on the provided documents."

## How It Works

### 1. Loading Documents
The system reads all `.txt` files from the `docs` folder.

### 2. Splitting Text
Long documents are split into chunks of ~500 characters. This makes searching easier.

### 3. Creating Embeddings
Each chunk is converted to numbers (embeddings) using model `all-MiniLM-L6-v2`. Similar text has similar numbers.

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

### The responses are slow(taking 10-12 minutes for one question, so please wait till Loading... completes)

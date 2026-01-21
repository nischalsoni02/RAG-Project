from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_store = None

class Question(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str
    sources: list[str]

# Load all documents from the docs folder
def load_documents():
    loader = DirectoryLoader(
        './docs',
        glob="*.txt",
        loader_cls=TextLoader
    )
    documents = loader.load()
    return documents

# Split documents into smaller chunks
def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = text_splitter.split_documents(documents)
    return chunks

# Create embeddings and store in FAISS
def create_vector_store(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store

# Create the RAG chain with LLaMA
def create_rag_chain(vector_store):
    

    prompt_template = """You are a cybersecurity assistant. Answer the question based ONLY on the following context.
If the answer is not in the context, say "I don't know based on the provided documents."
Do not use any outside knowledge.

Context: {context}

Question: {question}

Answer:"""

    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )

    llm = Ollama(model="llama3", temperature=0)

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
        return_source_documents=True,
        chain_type_kwargs={"prompt": prompt}
    )

    return qa_chain

# Initialize the RAG system when the server starts
@app.on_event("startup")
async def startup_event():
    
    global vector_store

    print("Loading documents...")
    documents = load_documents()
    print(f"Loaded {len(documents)} documents")

    print("Splitting documents into chunks...")
    chunks = split_documents(documents)
    print(f"Created {len(chunks)} chunks")

    print("Creating embeddings and vector store...")
    vector_store = create_vector_store(chunks)
    print("RAG system ready!")

@app.get("/")
async def root():
    return {"message": "Cybersecurity RAG API is running"}

@app.post("/ask", response_model=Answer)
async def ask_question(question: Question):
    """Answer a question using RAG"""

    if vector_store is None:
        return Answer(
            answer="System is still initializing. Please wait.",
            sources=[]
        )

    qa_chain = create_rag_chain(vector_store)

    result = qa_chain.invoke({"query": question.question})

    answer_text = result["result"]
    source_docs = result["source_documents"]

    source_files = []
    for doc in source_docs:
        source_file = os.path.basename(doc.metadata.get("source", "unknown"))
        if source_file not in source_files:
            source_files.append(source_file)

    return Answer(
        answer=answer_text,
        sources=source_files
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

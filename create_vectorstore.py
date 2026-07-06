import os
from dotenv import load_dotenv

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

# ---------------- PATH ----------------
DATA_PATH = "data"
DB_FAISS_PATH = "vectorstore/db_faiss"

# ---------------- LOAD PDFS ----------------
loader = DirectoryLoader(
    DATA_PATH,
    glob="*.pdf",
    loader_cls=PyPDFLoader
)

documents = loader.load()

print(f"Total Pages Loaded: {len(documents)}")

# ---------------- SPLIT DOCUMENTS ----------------
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

text_chunks = text_splitter.split_documents(documents)

# ---------------- ADD METADATA ----------------
for chunk in text_chunks:
    source = chunk.metadata.get("source", "")
    pdf_name = os.path.splitext(os.path.basename(source))[0].lower()

    if "passport" in pdf_name:
        chunk.metadata["scheme"] = "passport"

    elif "ayushman" in pdf_name:
        chunk.metadata["scheme"] = "ayushman"

    elif "pm" in pdf_name and "kisan" in pdf_name:
        chunk.metadata["scheme"] = "pm_kisan"

    elif "aadhaar" in pdf_name or "aadhar" in pdf_name:
        chunk.metadata["scheme"] = "aadhaar"

    else:
        chunk.metadata["scheme"] = "other"

print(f"Total Chunks Created: {len(text_chunks)}")

# ---------------- EMBEDDINGS ----------------
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ---------------- CREATE VECTOR STORE ----------------
db = FAISS.from_documents(
    text_chunks,
    embedding_model
)

# ---------------- SAVE ----------------
db.save_local(DB_FAISS_PATH)

print("✅ FAISS Vector Store Created Successfully!")
<<<<<<< HEAD
# 🇮🇳 Government Scheme AI Assistant

An AI-powered chatbot that answers questions about Indian Government Schemes using **Retrieval-Augmented Generation (RAG)**. The assistant retrieves information from official government PDF documents and generates accurate, context-based responses using the **Groq Llama 3.1** Large Language Model.

---

# 📌 Overview

The Government Scheme AI Assistant helps users access reliable information about various Government of India schemes without manually searching lengthy PDF documents.

Instead of relying solely on an LLM's general knowledge, the chatbot retrieves relevant information from official government documents stored in a FAISS vector database and then generates answers based on the retrieved content.

---

# ✨ Features

- 📄 Answers questions using official Government PDF documents
- 🔍 Retrieval-Augmented Generation (RAG)
- 🧠 Semantic Search using FAISS Vector Database
- 🤖 Powered by Groq Llama 3.1
- ⚡ Fast response generation
- 💬 Interactive Streamlit chatbot
- 📚 Supports multiple Government Schemes
- 🔒 Generates responses using retrieved document context

---

# 🏛 Supported Government Services

- Passport Seva
- Aadhaar (UIDAI)
- PM-KISAN
- Ayushman Bharat (PM-JAY)
- Other Government Scheme documents

---

# 🛠 Tech Stack

- Python
- Streamlit
- LangChain
- Groq API
- FAISS
- HuggingFace Embeddings
- Sentence Transformers
- PyPDF
- Python Dotenv

---

# 📂 Project Structure

```text
Government-Scheme-Assistant/
│
├── data/
│   ├── Passport.pdf
│   ├── Aadhaar.pdf
│   ├── PM-KISAN.pdf
│   ├── Ayushman Bharat.pdf
│   └── ...
│
├── vectorstore/
│   └── db_faiss/
│
├── create_vectorstore.py
├── rag_chain.py
├── app.py
├── requirements.txt
├── .env
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/varshachavan629-spec/Government-Scheme-Assistant.git

cd Government-Scheme-Assistant
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

or

```bash
uv pip install -r requirements.txt
```

---

## 4️⃣ Create Environment File

Create a `.env` file inside the project directory.

```env
GROQ_API_KEY=your_groq_api_key
```

---

# 📄 Add Government Documents

Place all official Government PDF documents inside the `data/` folder.

Example:

- Passport User Guide
- Passport FAQs
- Aadhaar Guidelines
- PM-KISAN Guidelines
- Ayushman Bharat Guidelines
- Other Government Scheme PDFs

---

# 🧠 Create Vector Store

Run:

```bash
python create_vectorstore.py
```

This script will:

- Load PDF documents
- Split documents into text chunks
- Generate embeddings
- Store embeddings in the FAISS vector database

---

# 🔍 Test the RAG Pipeline

Run:

```bash
python rag_chain.py
```

The script will:

- Accept a user question
- Retrieve relevant document chunks from FAISS
- Send the retrieved context to Groq LLM
- Generate an answer based on the retrieved documents

---

# ▶️ Run the Web Application

```bash
streamlit run app.py
```

Open your browser and visit:

```
http://localhost:8501
```

---

# 💬 Example Questions

## Passport

- What is Passport?
- What documents are required for Passport?
- How can I renew my Passport?
- What is ECR?
- What is Non-ECR?

---

## Aadhaar

- What is Aadhaar?
- How can I update my Aadhaar?
- What documents are required for Aadhaar enrollment?
- How can I download e-Aadhaar?

---

## PM-KISAN

- What is PM-KISAN?
- Who is eligible for PM-KISAN?
- What benefits are provided?
- How can farmers apply?

---

## Ayushman Bharat

- What is Ayushman Bharat?
- What are the benefits?
- How can I check my eligibility?
- Can I receive treatment in private hospitals?

---

# 🧠 RAG Workflow

```text
Government PDF Documents
            │
            ▼
      Document Loader
            │
            ▼
      Text Splitter
            │
            ▼
Generate HuggingFace Embeddings
            │
            ▼
      FAISS Vector Store
            │
            ▼
─────────────────────────────────
            │
            ▼
      User Question
            │
            ▼
Semantic Search in FAISS
            │
            ▼
Relevant Document Chunks
            │
            ▼
Prompt Template
            │
            ▼
Groq Llama 3.1
            │
            ▼
Generated Answer
```

---

# 📚 Data Sources

This chatbot uses official Government of India documents, including:

- Passport Seva
- UIDAI (Aadhaar)
- PM-KISAN
- Ayushman Bharat (PM-JAY)
- Other official Government Scheme documents

---

# 🚀 Future Enhancements

- Context-aware conversation memory
- Source citations with page numbers
- Multi-language support
- Voice interaction
- OCR support for scanned PDFs
- User feedback system
- Authentication
- Cloud deployment

---

# 👩‍💻 Author

**Varsha Chavan**

**GitHub**

https://github.com/varshachavan629-spec

**LinkedIn**

https://www.linkedin.com/in/varsha-chavan-54838b2b1

---

# 📄 License

This project is developed for educational and learning purposes.

---

⭐ If you found this project useful, consider giving it a **Star** on GitHub.
=======
# Government-Scheme-Assistant
AI-powered RAG chatbot for Indian Government Schemes using LangChain, FAISS, Groq, and Streamlit
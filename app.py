import os
import streamlit as st
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ---------------- LOAD ENV ----------------
load_dotenv()

st.set_page_config(
    page_title="Gov AI Assistant",
    page_icon="🇮🇳",
    layout="wide"
)

# ---------------- CUSTOM HEADER ----------------
st.markdown("""
    <style>
        .main-title {
            font-size: 40px;
            font-weight: bold;
            background: linear-gradient(90deg,#00C9FF,#92FE9D);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .chat-box {
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 10px;
        }

        .user {
            background-color: #DCF8C6;
            text-align: right;
        }

        .bot {
            background-color: #F1F0F0;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-title'>🇮🇳 Government Scheme AI Assistant</div>", unsafe_allow_html=True)
st.caption("Ask anything about PM-KISAN, Aadhaar, Passport, Ayushman Bharat")

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("⚙️ Settings")
    st.write("📌 Powered by Groq + FAISS")
    st.success("AI Assistant Ready")

    if st.button("🧹 Clear Chat"):
        st.session_state.messages = []

# ---------------- LLM ----------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
    max_tokens=512,
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------- VECTOR DB ----------------
db = FAISS.load_local(
    "vectorstore/db_faiss",
    HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(search_kwargs={"k": 4})

# ---------------- CHAT MEMORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

def format_docs(docs):
    return "\n\n".join(d.page_content for d in docs)

def get_history():
    return "\n".join(
        f"{m['role']}: {m['content']}" for m in st.session_state.messages[-6:]
    )

# ---------------- PROMPTS ----------------
rewrite_prompt = ChatPromptTemplate.from_template("""
Rewrite question clearly using chat history if needed.

Chat:
{chat_history}

Question:
{question}
""")

rewrite_chain = rewrite_prompt | llm | StrOutputParser()

final_prompt = ChatPromptTemplate.from_template("""
You are a Government Scheme Assistant.

Use ONLY context.

Chat:
{chat_history}

Context:
{context}

Question:
{question}

Answer in short, clear points.
""")

# ---------------- DISPLAY CHAT ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- INPUT ----------------
query = st.chat_input("Ask about government schemes...")

if query:

    st.session_state.messages.append({"role": "user", "content": query})

    with st.chat_message("user"):
        st.markdown(query)

    history = get_history()

    # rewrite
    rewritten = rewrite_chain.invoke({
        "chat_history": history,
        "question": query
    }).strip()

    # retrieve
    docs = retriever.invoke(rewritten)
    context = format_docs(docs)

    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤖"):
            answer = (final_prompt | llm | StrOutputParser()).invoke({
                "chat_history": history,
                "context": context,
                "question": rewritten
            })

            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer});
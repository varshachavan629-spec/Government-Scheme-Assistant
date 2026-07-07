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

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Government Scheme AI Assistant",
    page_icon="🇮🇳",
    layout="wide"
)

# ---------------- LOAD CSS ----------------
def load_css():
    with open("style.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# ---------------- HERO SECTION ----------------
st.markdown("""
<div class="hero-card">

<div style="font-size:65px;text-align:center;">🇮🇳</div>

<div class="main-title">
Government Scheme AI Assistant
</div>

<div class="subtitle">
Your trusted AI assistant for Indian Government Schemes.<br>
Ask about <b>PM-KISAN</b>, <b>Ayushman Bharat</b>,
<b>Aadhaar</b>, <b>Passport</b>,
<b>Scholarships</b>, and many more.
</div>

</div>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.markdown("""
    <div class="sidebar-title">
    🏛 Government AI
    </div>

    <div class="sidebar-sub">
    Powered by Groq • LangChain • FAISS
    </div>

    <div class="status-card">
    🟢 AI Assistant Ready
    </div>
    """, unsafe_allow_html=True)

    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = []

    st.markdown("---")

    st.markdown("### Popular Schemes")

    st.markdown("""
    <div class="suggestion">🌾 PM-KISAN</div>
    <div class="suggestion">🏥 Ayushman Bharat</div>
    <div class="suggestion">🆔 Aadhaar</div>
    <div class="suggestion">🛂 Passport</div>
    <div class="suggestion">🎓 Scholarships</div>
    """, unsafe_allow_html=True)

# ---------------- LLM ----------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.2,
    max_tokens=512,
    api_key=os.getenv("GROQ_API_KEY")
)

# ---------------- VECTOR DATABASE ----------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    "vectorstore/db_faiss",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(search_kwargs={"k": 4})

# ---------------- SESSION ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- HELPERS ----------------
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_history():
    return "\n".join(
        f"{msg['role']}: {msg['content']}"
        for msg in st.session_state.messages[-6:]
    )

# ---------------- PROMPTS ----------------
rewrite_prompt = ChatPromptTemplate.from_template("""
Rewrite the question clearly using the chat history if required.

Chat History:
{chat_history}

Question:
{question}
""")

rewrite_chain = rewrite_prompt | llm | StrOutputParser()

final_prompt = ChatPromptTemplate.from_template("""
You are an AI assistant for Indian Government Schemes.

Answer ONLY from the provided context.

Chat History:
{chat_history}

Context:
{context}

Question:
{question}

Give a concise answer using bullet points wherever appropriate.
""")

# ---------------- CHAT HISTORY ----------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------- CHAT INPUT ----------------
query = st.chat_input("💬 Ask about any Government Scheme...")

if query:

    st.session_state.messages.append(
        {"role": "user", "content": query}
    )

    with st.chat_message("user"):
        st.markdown(query)

    history = get_history()

    rewritten_query = rewrite_chain.invoke({
        "chat_history": history,
        "question": query
    }).strip()

    docs = retriever.invoke(rewritten_query)

    context = format_docs(docs)

    with st.chat_message("assistant"):

        with st.spinner("Searching Government Schemes..."):

            answer = (
                final_prompt
                | llm
                | StrOutputParser()
            ).invoke({
                "chat_history": history,
                "context": context,
                "question": rewritten_query
            })

            st.markdown(answer)

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )





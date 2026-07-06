import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ---------------- LOAD ENV ----------------
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# ---------------- LLM ----------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0.3,   # 🔥 lower = more accurate for government data
    max_tokens=512,
    api_key=GROQ_API_KEY,
)

# ---------------- VECTOR DB ----------------
DB_FAISS_PATH = "vectorstore/db_faiss"

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.load_local(
    DB_FAISS_PATH,
    embedding_model,
    allow_dangerous_deserialization=True
)

retriever = db.as_retriever(search_kwargs={"k": 5})

# ---------------- FORMAT DOCS ----------------
def format_docs(docs):
    if not docs:
        return "No relevant documents found."
    return "\n\n".join(doc.page_content for doc in docs)

# ---------------- MEMORY ----------------
chat_history = []

def get_chat_history():
    return "\n".join([f"{role}: {msg}" for role, msg in chat_history])

# ---------------- QUERY REWRITER ----------------
rewrite_prompt = ChatPromptTemplate.from_template("""
You are rewriting follow-up questions.

Rules:
1. If the question already contains the scheme name, do NOT change it.
2. If the question contains words like "it", "this", "that", or "these", replace them with the scheme mentioned in the MOST RECENT conversation only.
3. Ignore older conversations.
4. Output ONLY the rewritten question.
5. Do not explain your reasoning.

Recent Conversation:
{chat_history}

Current Question:
{question}

Rewritten Question:
""")
rewrite_chain = rewrite_prompt | llm | StrOutputParser()
# ---------------- FINAL PROMPT ----------------
final_prompt = ChatPromptTemplate.from_template("""
You are a Government Scheme Assistant.

Use ONLY the provided context.

Chat History:
{chat_history}

Context:
{context}

Question:
{question}

Answer in simple and correct way:
""")

# ---------------- CHAT LOOP ----------------
print("Government Scheme Assistant (type 'exit' to stop)\n")

while True:
    user_query = input("You: ")

    if user_query.lower() == "exit":
        break

    # Get recent chat history
    history = "\n".join(
        [f"{role}: {msg}" for role, msg in chat_history[-2:]]
    )

    # STEP 1: Rewrite question
    rewritten_question = rewrite_chain.invoke({
        "chat_history": history,
        "question": user_query
    }).strip()

    rewritten_question = rewritten_question.replace(
        "Rewritten Question:", ""
    ).strip()

    # STEP 2: Retrieve documents
    query = rewritten_question.lower()

    if "passport" in query:
        docs = db.similarity_search(
            rewritten_question,
            k=5,
            filter={"scheme": "passport"}
        )

    elif "ayushman" in query:
        docs = db.similarity_search(
            rewritten_question,
            k=5,
            filter={"scheme": "ayushman"}
        )

    elif (
        "pm kisan" in query
        or "pm-kisan" in query
        or "pm kissan" in query
        or "pm-kissan" in query
        or "kisan" in query
        or "kissan" in query
    ):
        docs = db.similarity_search(
            rewritten_question,
            k=5,
            filter={"scheme": "pm_kisan"}
        )

    elif "aadhaar" in query or "aadhar" in query:
        docs = db.similarity_search(
            rewritten_question,
            k=5,
            filter={"scheme": "aadhaar"}
        )

    else:
        docs = retriever.invoke(rewritten_question)

    context = format_docs(docs)

    if context == "No relevant documents found.":
        print("\nBot: I couldn't find this information in the provided government documents.\n")
        continue

    # STEP 3: Generate answer
    answer = (final_prompt | llm | StrOutputParser()).invoke({
        "chat_history": history,
        "context": context,
        "question": rewritten_question
    })

    print("\nBot:", answer, "\n")

    # Save conversation
    chat_history.append(("User", user_query))
    chat_history.append(("Assistant", answer))
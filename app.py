from flask import Flask, render_template, request, session
from src.helper import download_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.memory import ChatMessageHistory
from dotenv import load_dotenv
from src.prompt import *
import os

# ----------------- Flask Setup -----------------
app = Flask(__name__)
app.secret_key = "supersecretkey"  # For dev only. Use a secure key in production!

# ----------------- Load Environment -----------------
load_dotenv(dotenv_path="C:\\Users\\rohit rawat\\Desktop\\Gen_AI\\ROS_CHATBOT\\.env", override=True)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

# ----------------- Embeddings -----------------
embeddings = download_embeddings()

# ----------------- Pinecone Vector Store -----------------
index_name = "ros"
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# ----------------- LLM -----------------
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.6
)

# ----------------- History-Aware Retriever -----------------
contextualize_q_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that reformulates follow-up questions to be standalone."),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])
history_aware_retriever = create_history_aware_retriever(
    llm, retriever, contextualize_q_prompt
)

# ----------------- Main QA Chain -----------------
qa_prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}")
])
question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

# ----------------- Chat History Store -----------------
store = {}  # session_id -> ChatMessageHistory

def get_session_history(session_id: str) -> ChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

with_history = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer"
)

# ----------------- Routes -----------------
@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]

    if "session_id" not in session:
        session["session_id"] = os.urandom(8).hex()

    session_id = session["session_id"]

    response = with_history.invoke(
        {"input": msg},
        config={"configurable": {"session_id": session_id}}
    )

    return str(response["answer"])

# ----------------- Run -----------------
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)

from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.2)

def ask_question(query, chat_history=None):
    """
    chat_history: a list of (question, answer) tuples from earlier in the conversation.
    If None, treated as a fresh conversation with no prior context.
    """
    if chat_history is None:
        chat_history = []

    # Step A: Retrieve relevant chunks (same as before)
    results = vectorstore.similarity_search(query, k=6)
    context = "\n\n".join([doc.page_content for doc in results])

    # Step B: Build a history string from previous turns (if any)
    history_text = ""
    for past_question, past_answer in chat_history:
        history_text += f"Student: {past_question}\nAssistant: {past_answer}\n\n"

    # Step C: Build the prompt - now includes conversation history
    prompt = f"""You are a helpful assistant for UCER (United College of Engineering and Research) students.
Answer the student's question using ONLY the context below. If the answer isn't in the context, say you don't know - do not make up information.

If the student's question refers back to something discussed earlier in the conversation (e.g. "what about for them?", "and for 2nd year?"), use the conversation history below to understand what they're referring to.

Conversation history so far:
{history_text if history_text else "(no previous messages)"}

Context from documents:
{context}

Current question: {query}

Answer:"""

    response = llm.invoke(prompt)
    return response.content, results

# ---- Test it interactively in the terminal ----
if __name__ == "__main__":
    print("UCER Campus Assistant (type 'exit' to quit)\n")
    chat_history = []

    while True:
        query = input("Ask a question: ")
        if query.lower() == "exit":
            break

        answer, sources = ask_question(query, chat_history)

        print(f"\nAnswer: {answer}\n")
        print("Sources used:")
        for doc in sources:
            print(f"  - {doc.metadata.get('source')}, page {doc.metadata.get('page')}")
        print()

        # Save this turn into history so the next question has context
        chat_history.append((query, answer))
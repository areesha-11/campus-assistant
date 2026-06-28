from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

# Load the existing database (we're not rebuilding it, just connecting to it)
vectorstore = Chroma(persist_directory="chroma_db", embedding_function=embeddings)

# A test question - change this to something relevant to your actual documents
query = "What is the hostel fee?"

# This searches for the 3 most relevant chunks based on meaning, not keywords
results = vectorstore.similarity_search(query, k=3)

print(f"Query: {query}\n")
for i, doc in enumerate(results, 1):
    print(f"--- Result {i} ---")
    print(f"Source: {doc.metadata.get('source')}, Page: {doc.metadata.get('page')}")
    print(doc.page_content[:300])
    print()
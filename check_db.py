from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

print("1")

load_dotenv()

print("2")

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

print("3")

vectorstore = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

print("4")

print(vectorstore._collection.count())

print("5")
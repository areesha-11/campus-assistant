from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

folders = ["data/regulations", "data/notices", "data/fees"]
all_documents = []

for folder in folders:
    for filename in os.listdir(folder):
        if filename.endswith(".pdf"):
            filepath = os.path.join(folder, filename)
            loader = PyPDFLoader(filepath)
            docs = loader.load()
            all_documents.extend(docs)

print(f"Total pages loaded: {len(all_documents)}")

# ---- NEW PART: Chunking ----

# RecursiveCharacterTextSplitter tries to split on paragraph breaks first,
# then sentences, then words — so chunks stay as semantically coherent as possible
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,      # roughly how many characters per chunk
    chunk_overlap=100,   # overlap so context isn't lost at chunk boundaries
    separators=["\n\n", "\n", ". ", " ", ""]  # tries these in order
)

chunks = text_splitter.split_documents(all_documents)

print(f"Total chunks created: {len(chunks)}")
print("\n---- Sample chunk ----")
print(chunks[0].page_content)
print("\n---- Sample chunk metadata ----")
print(chunks[0].metadata)
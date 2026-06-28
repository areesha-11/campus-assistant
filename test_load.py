from langchain_community.document_loaders import PyPDFLoader
import os

# All three folders we want to scan
folders = ["data/regulations", "data/notices", "data/fees"]

all_documents = []

for folder in folders:
    # List every file in this folder
    for filename in os.listdir(folder):
        if filename.endswith(".pdf"):
            filepath = os.path.join(folder, filename)
            print(f"Loading: {filepath}")
            
            loader = PyPDFLoader(filepath)
            docs = loader.load()
            
            all_documents.extend(docs)
            print(f"  -> {len(docs)} pages loaded")

print(f"\nTotal documents (pages) loaded across all PDFs: {len(all_documents)}")
print("\n---- Sample preview from first document ----")
print(all_documents[0].page_content[:500])
print("\n---- Sample metadata ----")
print(all_documents[0].metadata)
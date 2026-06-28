from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from dotenv import load_dotenv
import pytesseract
from pdf2image import convert_from_path
import os
import time

# Load the API key from .env into the environment
load_dotenv()

# ---- OCR setup ----
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
poppler_path = r"C:\poppler\poppler-26.02.0\Library\bin"

# These specific files are scanned/image-based and need OCR instead of normal PDF text extraction
OCR_FILES = [
    "Bus Registration.pdf",
    "Hostel Registration.pdf",
    "Fees1.pdf",
    "Fees2.pdf",
]

def ocr_pdf_to_documents(pdf_path):
    """Converts each page of a scanned PDF into an image, then OCRs it into a Document object."""
    pages = convert_from_path(pdf_path, poppler_path=poppler_path)
    documents = []
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page)
        # Wrap OCR'd text in a Document object, matching what PyPDFLoader normally produces,
        # so the rest of the pipeline (chunking, embeddings) treats it identically
        doc = Document(
            page_content=text,
            metadata={"source": pdf_path, "page": i}
        )
        documents.append(doc)
    return documents

# ---- Step 1: Load all PDFs from all folders ----

folders = ["data/regulations", "data/notices", "data/fees"]
all_documents = []

for folder in folders:
    for filename in os.listdir(folder):
        if filename.endswith(".pdf"):
            filepath = os.path.join(folder, filename)

            if filename in OCR_FILES:
                print(f"Loading with OCR: {filepath}")
                docs = ocr_pdf_to_documents(filepath)
            else:
                print(f"Loading: {filepath}")
                loader = PyPDFLoader(filepath)
                docs = loader.load()

            all_documents.extend(docs)
            print(f"  -> {len(docs)} pages loaded")

print(f"\nTotal pages loaded: {len(all_documents)}")

# ---- Step 2: Chunk the documents ----

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " ", ""]
)

chunks = text_splitter.split_documents(all_documents)
print(f"Total chunks created: {len(chunks)}")

# ---- Step 3: Generate embeddings + store in ChromaDB (Google Gemini - free) ----

embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

print("\nGenerating embeddings and storing in ChromaDB... this will take a few minutes")

batch_size = 80  # stay safely under the 100/minute free-tier limit
vectorstore = None

for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i + batch_size]
    batch_number = i // batch_size + 1
    total_batches = (len(chunks) // batch_size) + 1
    print(f"Processing batch {batch_number} of {total_batches} ({len(batch)} chunks)...")

    if vectorstore is None:
        vectorstore = Chroma.from_documents(
            documents=batch,
            embedding=embeddings,
            persist_directory="chroma_db"
        )
    else:
        vectorstore.add_documents(batch)

    if i + batch_size < len(chunks):
        print("Waiting 60 seconds to respect rate limit...")
        time.sleep(60)

print("\nDone! Vector database saved to ./chroma_db")
print(f"Total vectors stored: {vectorstore._collection.count()}")
import pytesseract
from pdf2image import convert_from_path

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
poppler_path = r"C:\poppler\poppler-26.02.0\Library\bin"

def ocr_pdf(pdf_path):
    pages = convert_from_path(pdf_path, poppler_path=poppler_path)
    full_text = ""
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page)
        full_text += f"\n--- Page {i+1} ---\n{text}"
    return full_text

files_to_test = [
    "data/fees/Bus Registration.pdf",
    "data/fees/Hostel Registration.pdf",
    "data/fees/Fees1.pdf",
    "data/fees/Fees2.pdf",
]

for filepath in files_to_test:
    print(f"\n========== {filepath} ==========")
    text = ocr_pdf(filepath)
    print(text[:800])  # just a preview, first 800 characters
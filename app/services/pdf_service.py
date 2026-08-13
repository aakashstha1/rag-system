from pypdf import PdfReader

# Take a PDF path → extract its text → return that text 
# file_path: str means it's a string
# -> str means it returns a string
def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text
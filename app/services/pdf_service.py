from pypdf import PdfReader

# Function to extract all text from a PDF file
# file_path: path to the PDF file
# returns: extracted text as a string
def extract_text_from_pdf(file_path: str) -> str:
    
    # Open the PDF file
    reader = PdfReader(file_path)

    text = ""

    # Loop through each page in the PDF
    for page in reader.pages:
        
        # Extract text from the page and add it to text
        # "or ''" prevents errors if a page has no text
        text += page.extract_text() or ""

    return text
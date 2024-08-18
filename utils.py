from pypdf import PdfReader

def extract_text_from_pdf(uploaded_file):
    text = ""
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text()
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {e}")
    return text

import os

def extract_text_from_file(file_path):
    """
    Extract text content from PDF or DOCX files.
    """
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    
    if ext == '.pdf':
        try:
            import pypdf
            reader = pypdf.PdfReader(file_path)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception as e:
            text = f"[Could not parse PDF file directly: {e}]"
            
    elif ext == '.docx':
        try:
            import docx
            doc = docx.Document(file_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            text = "\n".join(full_text)
        except Exception as e:
            text = f"[Could not parse DOCX file directly: {e}]"
    else:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
        except Exception:
            text = "[Unsupported file format]"
            
    return text.strip()

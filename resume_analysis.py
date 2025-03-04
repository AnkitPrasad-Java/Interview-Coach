import fitz  # PyMuPDF for PDF text extraction
import ollama  # AI model for resume analysis

def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file"""
    doc = fitz.open(pdf_file)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def analyze_resume(resume_text):
    """Uses Ollama AI to analyze the resume"""
    model = "mistral"  # Ollama model
    prompt = f"""
    You are an expert resume analyst. Evaluate the following resume content:
    
    {resume_text}

    Provide:
    1️⃣ Strengths in resume
    2️⃣ Weaknesses or areas of improvement
    3️⃣ Suggested improvements to make it ATS-friendly
    4️⃣ Score out of 10 based on industry standards
    """

    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response['message']['content']

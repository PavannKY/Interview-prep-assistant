"""
Resume Parsing Service
PDF/DOCX extraction → structured JSON via small local LLM (Ollama)
"""
import os
import pdfplumber
import docx
from pathlib import Path
from utils.llm_client import get_client, LLM_MODEL, extract_json
from models.schemas import ParsedResume


def extract_text_from_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text.strip()


def extract_text_from_docx(file_path: str) -> str:
    doc = docx.Document(file_path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_text(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif ext in (".docx", ".doc"):
        return extract_text_from_docx(file_path)
    raise ValueError(f"Unsupported file type: {ext}")


PARSE_PROMPT = """Extract information from this resume and return ONLY a JSON object.
No explanation, no markdown, just the raw JSON.

JSON format:
{{
  "name": "Full Name or null",
  "email": "email or null",
  "phone": "phone or null",
  "summary": "brief professional summary or null",
  "skills": ["skill1", "skill2"],
  "experience": [
    {{"title": "Job Title", "company": "Company", "duration": "dates", "description": "what they did"}}
  ],
  "education": [
    {{"degree": "Degree Name", "institution": "University", "year": "year"}}
  ],
  "projects": [
    {{"name": "Project", "description": "what it does", "tech_stack": ["tech1"]}}
  ],
  "certifications": ["cert1"]
}}

Resume:
{resume_text}

JSON:"""


async def parse_resume_with_llm(raw_text: str) -> dict:
    client = get_client()
    response = await client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": PARSE_PROMPT.format(resume_text=raw_text[:4000])}],
        temperature=0.1,
        max_tokens=1500,
    )
    return extract_json(response.choices[0].message.content)


async def parse_resume(file_path: str) -> ParsedResume:
    raw_text = extract_text(file_path)
    structured = await parse_resume_with_llm(raw_text)
    return ParsedResume(
        raw_text=raw_text,
        name=structured.get("name"),
        email=structured.get("email"),
        phone=structured.get("phone"),
        summary=structured.get("summary"),
        skills=structured.get("skills", []),
        experience=structured.get("experience", []),
        education=structured.get("education", []),
        projects=structured.get("projects", []),
        certifications=structured.get("certifications", []),
    )

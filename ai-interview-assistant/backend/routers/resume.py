"""
Resume Upload Router
POST /resume/upload  → parses resume, creates session, returns structured data
"""
import os
import uuid
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path

from services.resume_parser import parse_resume
from utils.session_store import create_session, update_session, get_session
from models.schemas import ResumeUploadResponse

router = APIRouter(prefix="/resume", tags=["Resume"])

UPLOAD_DIR = Path(os.getenv("RESUME_UPLOAD_DIR", "./data/resumes"))
ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc"}
MAX_FILE_SIZE_MB = 10


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    """
    Upload a resume (PDF or DOCX).
    Returns session_id and structured resume data.
    """
    # Validate extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Upload a PDF or DOCX."
        )

    # Create session
    session_id = str(uuid.uuid4())
    save_path = UPLOAD_DIR / f"{session_id}{ext}"
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Save file
    try:
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File save failed: {e}")

    # Parse
    try:
        parsed = await parse_resume(str(save_path))
    except Exception as e:
        save_path.unlink(missing_ok=True)
        raise HTTPException(status_code=422, detail=f"Resume parsing failed: {e}")

    # Persist session
    session = create_session(session_id)
    session.resume = parsed
    update_session(session)

    return ResumeUploadResponse(
        session_id=session_id,
        filename=file.filename,
        parsed=parsed,
        message="Resume uploaded and parsed successfully.",
    )


@router.get("/{session_id}")
async def get_resume(session_id: str):
    """Retrieve the parsed resume for a session."""
    session = get_session(session_id)
    if not session or not session.resume:
        raise HTTPException(status_code=404, detail="Session not found.")
    return session.resume

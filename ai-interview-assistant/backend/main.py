"""
AI Interview Assistant - FastAPI Backend
Entry point: uvicorn main:app --reload
"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from routers import resume, interview, feedback

app = FastAPI(
    title="AI Interview Assistant",
    description="Resume-aware AI interviewer with skill gap analysis",
    version="1.0.0",
)

# ─── CORS ─────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("FRONTEND_URL", "http://localhost:5173"), "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Routers ──────────────────────────────────────────────────────────────────
app.include_router(resume.router)
app.include_router(interview.router)
app.include_router(feedback.router)


@app.get("/")
async def root():
    return {
        "message": "AI Interview Assistant API",
        "docs": "/docs",
        "version": "1.0.0",
    }


@app.get("/health")
async def health():
    return {"status": "ok"}

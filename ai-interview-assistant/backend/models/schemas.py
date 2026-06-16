from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


# ─── Resume Models ────────────────────────────────────────────────────────────

class ParsedResume(BaseModel):
    raw_text: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: List[str] = []
    experience: List[dict] = []       # [{title, company, duration, description}]
    education: List[dict] = []        # [{degree, institution, year}]
    projects: List[dict] = []         # [{name, description, tech_stack}]
    certifications: List[str] = []
    summary: Optional[str] = None


class ResumeUploadResponse(BaseModel):
    session_id: str
    filename: str
    parsed: ParsedResume
    message: str


# ─── Interview Models ──────────────────────────────────────────────────────────

class DifficultyLevel(str, Enum):
    easy = "easy"
    medium = "medium"
    hard = "hard"


class InterviewQuestion(BaseModel):
    id: str
    question: str
    topic: str                  # e.g. "Python", "System Design", "Behavioural"
    difficulty: DifficultyLevel
    expected_concepts: List[str] = []


class QuestionsResponse(BaseModel):
    session_id: str
    questions: List[InterviewQuestion]
    total: int


class AnswerSubmit(BaseModel):
    session_id: str
    question_id: str
    question_text: str
    answer: str


class AnswerEvaluation(BaseModel):
    question_id: str
    score: int                  # 0–10
    feedback: str
    strengths: List[str]
    improvements: List[str]
    concepts_covered: List[str]
    concepts_missing: List[str]


# ─── Interview Session State ───────────────────────────────────────────────────

class SessionState(BaseModel):
    session_id: str
    resume: Optional[ParsedResume] = None
    questions: List[InterviewQuestion] = []
    answers: List[dict] = []            # [{question_id, answer, evaluation}]
    current_index: int = 0
    completed: bool = False


# ─── Feedback Models ──────────────────────────────────────────────────────────

class SkillGap(BaseModel):
    skill: str
    current_level: str          # "none" | "basic" | "intermediate" | "advanced"
    required_level: str
    resources: List[str] = []


class FinalFeedback(BaseModel):
    session_id: str
    overall_score: float        # 0–10
    performance_summary: str
    strongest_areas: List[str]
    weakest_areas: List[str]
    skill_gaps: List[SkillGap]
    resume_feedback: List[str]
    learning_roadmap: List[dict]   # [{week, focus, resources}]
    interview_ready: bool

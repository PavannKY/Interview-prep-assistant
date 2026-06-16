"""
Interview Router
GET  /interview/{session_id}/questions  → generate questions from resume
POST /interview/{session_id}/answer     → submit answer, get evaluation
GET  /interview/{session_id}/state      → get current session state
"""
from fastapi import APIRouter, HTTPException
from models.schemas import (
    QuestionsResponse,
    AnswerSubmit,
    AnswerEvaluation,
    SessionState,
)
from services.question_generator import generate_questions
from services.evaluator import evaluate_answer
from utils.session_store import get_session, update_session

router = APIRouter(prefix="/interview", tags=["Interview"])


@router.get("/{session_id}/questions", response_model=QuestionsResponse)
async def get_questions(session_id: str, num_questions: int = 10):
    """
    Generate personalized interview questions from the uploaded resume.
    Call this once after uploading a resume.
    """
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if not session.resume:
        raise HTTPException(status_code=400, detail="No resume found in this session.")

    # Generate only if not already done
    if not session.questions:
        questions = await generate_questions(session.resume, num_questions=num_questions)
        session.questions = questions
        update_session(session)

    return QuestionsResponse(
        session_id=session_id,
        questions=session.questions,
        total=len(session.questions),
    )


@router.post("/{session_id}/answer", response_model=AnswerEvaluation)
async def submit_answer(session_id: str, payload: AnswerSubmit):
    """
    Submit an answer to a question. Returns immediate evaluation.
    """
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")

    # Find the question
    question = next(
        (q for q in session.questions if q.id == payload.question_id), None
    )
    if not question:
        raise HTTPException(status_code=404, detail="Question not found.")

    # Evaluate
    evaluation = await evaluate_answer(
        question_id=payload.question_id,
        question_text=payload.question_text,
        answer=payload.answer,
        expected_concepts=question.expected_concepts,
    )

    # Store in session
    session.answers.append({
        "question_id": payload.question_id,
        "answer": payload.answer,
        "evaluation": evaluation.model_dump(),
    })
    session.current_index += 1

    # Mark complete if all answered
    if session.current_index >= len(session.questions):
        session.completed = True

    update_session(session)
    return evaluation


@router.get("/{session_id}/state", response_model=SessionState)
async def get_state(session_id: str):
    """Get the full current state of an interview session."""
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    return session

"""
Feedback Router
GET /feedback/{session_id}  → generate full final report
"""
from fastapi import APIRouter, HTTPException
from models.schemas import FinalFeedback, AnswerEvaluation
from services.feedback import generate_final_feedback
from utils.session_store import get_session

router = APIRouter(prefix="/feedback", tags=["Feedback"])


@router.get("/{session_id}", response_model=FinalFeedback)
async def get_feedback(session_id: str):
    """
    Generate the final interview report.
    Requires all (or most) questions to have been answered.
    """
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if not session.resume:
        raise HTTPException(status_code=400, detail="No resume in session.")
    if not session.answers:
        raise HTTPException(status_code=400, detail="No answers submitted yet.")

    evaluations = [
        AnswerEvaluation(**a["evaluation"]) for a in session.answers
    ]

    # Map back to question objects
    answered_ids = {a["question_id"] for a in session.answers}
    answered_questions = [q for q in session.questions if q.id in answered_ids]

    feedback = await generate_final_feedback(
        session_id=session_id,
        resume=session.resume,
        questions=answered_questions,
        evaluations=evaluations,
    )
    return feedback

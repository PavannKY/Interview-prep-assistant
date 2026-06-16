"""
Session Store
Simple in-memory session management for MVP.
Replace with Redis or PostgreSQL for production.
"""
from typing import Dict, Optional
from models.schemas import SessionState


_sessions: Dict[str, SessionState] = {}


def create_session(session_id: str) -> SessionState:
    session = SessionState(session_id=session_id)
    _sessions[session_id] = session
    return session


def get_session(session_id: str) -> Optional[SessionState]:
    return _sessions.get(session_id)


def update_session(session: SessionState) -> None:
    _sessions[session.session_id] = session


def delete_session(session_id: str) -> None:
    _sessions.pop(session_id, None)


def list_sessions() -> list:
    return list(_sessions.keys())

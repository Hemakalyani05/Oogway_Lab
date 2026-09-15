"""
Session management API routes.
"""
from typing import List, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy import desc

from app.api.deps import get_db
from app.db.models import SessionModel, MessageModel
from app.db.session import db_execute, db_commit, db_refresh, db_delete
from app.schemas.session import SessionCreate, SessionSummary, SessionDetail
from app.schemas.chat import ChatMessage, Citation
from app.core.logging import logger

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.get("", response_model=List[SessionSummary])
async def list_sessions(
    user_id: str = "default_user",
    db: Any = Depends(get_db)
):
    """Lists all chat sessions for a given user."""
    stmt = (
        select(SessionModel)
        .where(SessionModel.user_id == user_id)
        .order_by(desc(SessionModel.updated_at))
    )
    result = await db_execute(db, stmt)
    sessions = result.scalars().all()

    summaries = []
    for s in sessions:
        msg_stmt = select(MessageModel).where(MessageModel.session_id == s.id)
        msg_result = await db_execute(db, msg_stmt)
        msgs = msg_result.scalars().all()

        summaries.append(SessionSummary(
            id=s.id,
            title=s.title,
            user_id=s.user_id,
            active_model=s.active_model,
            message_count=len(msgs),
            created_at=s.created_at,
            updated_at=s.updated_at
        ))
    return summaries


@router.post("", response_model=SessionDetail, status_code=status.HTTP_201_CREATED)
async def create_session(
    payload: SessionCreate,
    db: Any = Depends(get_db)
):
    """Creates a new chat session."""
    new_session = SessionModel(
        title=payload.title or "New Conversation",
        user_id=payload.user_id or "default_user",
        active_model=payload.active_model or "mock"
    )
    db.add(new_session)
    await db_commit(db)
    await db_refresh(db, new_session)

    return SessionDetail(
        id=new_session.id,
        title=new_session.title,
        user_id=new_session.user_id,
        active_model=new_session.active_model,
        messages=[],
        created_at=new_session.created_at,
        updated_at=new_session.updated_at
    )


@router.get("/{session_id}", response_model=SessionDetail)
async def get_session_detail(
    session_id: str,
    db: Any = Depends(get_db)
):
    """Retrieves session details and its ordered message history."""
    stmt = select(SessionModel).where(SessionModel.id == session_id)
    result = await db_execute(db, stmt)
    session_obj = result.scalars().first()

    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")

    msg_stmt = (
        select(MessageModel)
        .where(MessageModel.session_id == session_id)
        .order_by(MessageModel.created_at)
    )
    msg_result = await db_execute(db, msg_stmt)
    messages_db = msg_result.scalars().all()

    chat_messages = []
    for m in messages_db:
        citations = []
        if m.citations and isinstance(m.citations, list):
            for c in m.citations:
                citations.append(Citation(**c))
        chat_messages.append(ChatMessage(
            role=m.role,
            content=m.content,
            citations=citations,
            created_at=m.created_at.isoformat()
        ))

    return SessionDetail(
        id=session_obj.id,
        title=session_obj.title,
        user_id=session_obj.user_id,
        active_model=session_obj.active_model,
        messages=chat_messages,
        created_at=session_obj.created_at,
        updated_at=session_obj.updated_at
    )


@router.delete("/{session_id}", status_code=status.HTTP_200_OK)
async def delete_session(
    session_id: str,
    db: Any = Depends(get_db)
):
    """Deletes a session and associated records."""
    stmt = select(SessionModel).where(SessionModel.id == session_id)
    result = await db_execute(db, stmt)
    session_obj = result.scalars().first()

    if not session_obj:
        raise HTTPException(status_code=404, detail="Session not found")

    await db_delete(db, session_obj)
    await db_commit(db)
    return {"status": "deleted", "session_id": session_id}

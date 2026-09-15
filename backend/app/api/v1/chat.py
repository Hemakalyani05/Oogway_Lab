"""
Chat and Streaming SSE API endpoints.
"""
from typing import AsyncGenerator, Any
import json
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.future import select

from app.api.deps import get_db
from app.db.models import SessionModel, MessageModel, ArtifactModel
from app.db.session import db_execute, db_commit, db_refresh
from app.schemas.chat import ChatRequest, ChatResponse, Citation
from app.agents.growth_agent import GrowthAgent
from app.core.logging import logger

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("")
async def chat_endpoint(
    payload: ChatRequest,
    db: Any = Depends(get_db)
):
    """
    Primary chat endpoint supporting Server-Sent Events (SSE) streaming.
    Streams tokens, retrieval citations, and generated artifacts in real-time.
    """
    session_id = payload.session_id
    if not session_id:
        new_session = SessionModel(
            title=payload.message[:40] + ("..." if len(payload.message) > 40 else ""),
            active_model=payload.provider or "mock"
        )
        db.add(new_session)
        await db_commit(db)
        await db_refresh(db, new_session)
        session_id = new_session.id
    else:
        stmt = select(SessionModel).where(SessionModel.id == session_id)
        result = await db_execute(db, stmt)
        session_obj = result.scalars().first()
        if not session_obj:
            new_session = SessionModel(
                id=session_id,
                title=payload.message[:40] + ("..." if len(payload.message) > 40 else ""),
                active_model=payload.provider or "mock"
            )
            db.add(new_session)
            await db_commit(db)

    # Fetch recent conversation history
    msg_stmt = (
        select(MessageModel)
        .where(MessageModel.session_id == session_id)
        .order_by(MessageModel.created_at)
    )
    msg_result = await db_execute(db, msg_stmt)
    prev_messages = msg_result.scalars().all()
    history = [{"role": m.role, "content": m.content} for m in prev_messages]

    # Persist User Message
    user_msg_db = MessageModel(
        id=str(uuid.uuid4()),
        session_id=session_id,
        role="user",
        content=payload.message
    )
    db.add(user_msg_db)
    await db_commit(db)

    # Growth Agent
    agent = GrowthAgent(provider_name=payload.provider, model_name=payload.model)

    async def sse_event_stream() -> AsyncGenerator[str, None]:
        yield f"data: {json.dumps({'type': 'session_init', 'session_id': session_id})}\n\n"

        collected_citations = []
        collected_raw_content = ""
        collected_clean_content = ""
        detected_artifact = None
        model_name_used = agent.provider.model_name

        try:
            async for event in agent.run_stream(
                user_message=payload.message,
                history=history,
                generate_ship30=payload.generate_ship30,
                generate_artifact=payload.generate_artifact
            ):
                if event["type"] == "citations":
                    collected_citations = event.get("citations", [])
                elif event["type"] == "done":
                    collected_clean_content = event.get("full_content", "")
                    collected_raw_content = event.get("raw_content", "")
                    detected_artifact = event.get("artifact")
                    model_name_used = event.get("model_used", model_name_used)

                yield f"data: {json.dumps(event)}\n\n"

            # Persist Assistant Response & Artifact
            try:
                assistant_msg_db = MessageModel(
                    id=str(uuid.uuid4()),
                    session_id=session_id,
                    role="assistant",
                    content=collected_clean_content or collected_raw_content,
                    citations=collected_citations,
                    model_used=model_name_used
                )
                db.add(assistant_msg_db)

                if detected_artifact and detected_artifact.get("is_valid"):
                    art_db = ArtifactModel(
                        id=str(uuid.uuid4()),
                        session_id=session_id,
                        title=detected_artifact["title"],
                        artifact_type=detected_artifact["artifact_type"],
                        language=detected_artifact["language"],
                        content=detected_artifact["content"],
                        metadata_json={"model": model_name_used}
                    )
                    db.add(art_db)

                stmt = select(SessionModel).where(SessionModel.id == session_id)
                res = await db_execute(db, stmt)
                s_obj = res.scalars().first()
                if s_obj:
                    s_obj.updated_at = datetime.now(timezone.utc)
                    db.add(s_obj)

                await db_commit(db)
            except Exception as save_err:
                logger.error(f"Error persisting assistant response: {save_err}")

        except Exception as stream_err:
            logger.error(f"Error in SSE stream: {stream_err}")
            yield f"data: {json.dumps({'type': 'error', 'message': str(stream_err)})}\n\n"

    return StreamingResponse(
        sse_event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )

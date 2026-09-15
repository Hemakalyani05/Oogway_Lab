"""
SQLAlchemy ORM Models for persistence of Sessions, Messages, Artifacts, and Transcripts.
"""
import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any

from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Float, JSON
from sqlalchemy.orm import relationship

from app.db.session import Base


def generate_uuid() -> str:
    return str(uuid.uuid4())


def utc_now():
    return datetime.now(timezone.utc)


class SessionModel(Base):
    """Represents an interactive conversation session."""
    __tablename__ = "sessions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False, default="New Conversation")
    user_id = Column(String(100), nullable=True, default="default_user")
    active_model = Column(String(100), nullable=False, default="mock")
    metadata_json = Column(JSON, nullable=True, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now, nullable=False)

    messages = relationship("MessageModel", back_populates="session", cascade="all, delete-orphan", order_by="MessageModel.created_at")
    artifacts = relationship("ArtifactModel", back_populates="session", cascade="all, delete-orphan", order_by="ArtifactModel.created_at")


class MessageModel(Base):
    """Represents a single message turn (user, assistant, or tool)."""
    __tablename__ = "messages"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    session_id = Column(String(36), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    role = Column(String(50), nullable=False)  # 'user', 'assistant', 'system'
    content = Column(Text, nullable=False)
    citations = Column(JSON, nullable=True, default=list)  # List of cited source objects
    token_usage = Column(JSON, nullable=True, default=dict)
    model_used = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    session = relationship("SessionModel", back_populates="messages")


class ArtifactModel(Base):
    """Represents generated standalone documents or interactive HTML/CSS components."""
    __tablename__ = "artifacts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    session_id = Column(String(36), ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    artifact_type = Column(String(50), nullable=False)  # 'markdown', 'html', 'css', 'javascript'
    language = Column(String(50), nullable=False, default="markdown")
    content = Column(Text, nullable=False)
    metadata_json = Column(JSON, nullable=True, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    session = relationship("SessionModel", back_populates="artifacts")


class TranscriptModel(Base):
    """Represents a complete ingested Lenny's Podcast episode."""
    __tablename__ = "transcripts"

    episode_id = Column(String(100), primary_key=True)
    title = Column(String(255), nullable=False)
    guest = Column(String(255), nullable=False)
    episode_url = Column(String(500), nullable=True)
    publication_date = Column(String(50), nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    chunks = relationship("TranscriptChunkModel", back_populates="transcript", cascade="all, delete-orphan")


class TranscriptChunkModel(Base):
    """Represents a searchable semantic chunk from an episode."""
    __tablename__ = "transcript_chunks"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    episode_id = Column(String(100), ForeignKey("transcripts.episode_id", ondelete="CASCADE"), nullable=False, index=True)
    chunk_index = Column(Integer, nullable=False)
    speaker = Column(String(255), nullable=True)
    timestamp_start = Column(String(50), nullable=True)
    timestamp_end = Column(String(50), nullable=True)
    content = Column(Text, nullable=False)
    embedding_json = Column(JSON, nullable=True)
    metadata_json = Column(JSON, nullable=True, default=dict)
    created_at = Column(DateTime(timezone=True), default=utc_now, nullable=False)

    transcript = relationship("TranscriptModel", back_populates="chunks")

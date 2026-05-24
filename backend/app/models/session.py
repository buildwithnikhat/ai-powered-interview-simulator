import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Integer, Float, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class CommunicationSession(Base):
    __tablename__ = "communication_sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"), nullable=False, index=True)
    session_type: Mapped[str] = mapped_column(String(50), nullable=False)
    transcript_text: Mapped[str] = mapped_column(Text, nullable=True)
    audio_file_path: Mapped[str] = mapped_column(String(500), nullable=True)
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0)
    fluency_score: Mapped[float] = mapped_column(Float, nullable=True)
    grammar_score: Mapped[float] = mapped_column(Float, nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=True)
    pronunciation_score: Mapped[float] = mapped_column(Float, nullable=True)
    filler_word_count: Mapped[int] = mapped_column(Integer, default=0)
    speaking_speed_wpm: Mapped[float] = mapped_column(Float, nullable=True)
    pause_count: Mapped[int] = mapped_column(Integer, default=0)
    agent_feedback: Mapped[str] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

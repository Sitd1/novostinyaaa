from __future__ import annotations
from datetime import datetime

from sqlalchemy import (
    String, Text, DateTime, ForeignKey
)
from sqlalchemy.orm import (
    Mapped, mapped_column, relationship
)
from sqlalchemy.sql import func
from database.models.base import Base

# ---------- News (новость) ----------
class News(Base):
    __tablename__ = "news"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    summary: Mapped[str | None] = mapped_column(Text)  # краткий лид/анонс
    source_name: Mapped[str | None] = mapped_column(String(120))
    source_url: Mapped[str | None] = mapped_column(String(500))
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    relevance_reasoning: Mapped[str] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))  # мягкое удаление (опц.)


    # FK + relationship на RunsStory

    # Foreign Key для связи с SearchRun
    run_fk: Mapped[int] = mapped_column(ForeignKey("search_runs.id"), nullable=False)

    # Relationship: многие новости принадлежат одному запуску поиска
    run: Mapped["RunsStory"] = relationship(back_populates="news_items")

    def __repr__(self):
        return f"<News(id={self.id}, title='{self.title}')>"

from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import (
    Integer,
    String,
    Text,
    DateTime,
    Enum as SAEnum,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.domain.news.value_objects import ImportanceLevel
from app.infrastructure.database.models.base import Base



class NewsEventORM(Base):
    __tablename__ = "news_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        server_default=func.now(), onupdate=func.now()
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)

    importance: Mapped[ImportanceLevel] = mapped_column(
        SAEnum(ImportanceLevel, name="importance_level"), nullable=False, index=True
    )

    # EventTime
    event_started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    event_ended_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )

    # Geography
    geo_country: Mapped[str | None] = mapped_column(String(64), nullable=True)
    geo_region: Mapped[str | None] = mapped_column(String(64), nullable=True)
    geo_city: Mapped[str | None] = mapped_column(String(128), nullable=True)

    user_interest_score: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # MANY raw news
    raw_news_links: Mapped[list["NewsEventRawNewsORM"]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    # MANY tags
    tags: Mapped[list["NewsEventTagORM"]] = relationship(
        back_populates="event",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<NewsEventORM id={self.id} title={self.title!r}>"


from __future__ import annotations

from sqlalchemy import (
    Integer,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.database.models.raw_news import RawNewsORM
from shared.database.models.base import Base



class NewsEventRawNewsORM(Base):
    __tablename__ = "news_event_raw_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    event_id: Mapped[int] = mapped_column(
        ForeignKey("news_events.id", ondelete="CASCADE"), nullable=False
    )
    raw_news_id: Mapped[int] = mapped_column(
        ForeignKey("tg_raw_news.id", ondelete="CASCADE"), nullable=False
    )

    event: Mapped["NewsEventORM"] = relationship(back_populates="raw_news_links")
    raw_news: Mapped["RawNewsORM"] = relationship()

    __table_args__ = (
        UniqueConstraint("event_id", "raw_news_id", name="uq_event_raw"),
    )


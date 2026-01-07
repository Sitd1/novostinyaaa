from __future__ import annotations

from sqlalchemy import (
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.database.models.base import Base

#
class NewsEventTagORM(Base):
    __tablename__ = "news_event_tags"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    event_id: Mapped[int] = mapped_column(
        ForeignKey("news_events.id", ondelete="CASCADE"), nullable=False
    )
    value: Mapped[str] = mapped_column(String(64), nullable=False, index=True)

    event: Mapped["NewsEventORM"] = relationship(back_populates="tags")

    __table_args__ = (
        UniqueConstraint("event_id", "value", name="uq_event_tag"),
    )

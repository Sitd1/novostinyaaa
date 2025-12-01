from __future__ import annotations
from datetime import datetime

from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base



class RunsStory(Base):
    __tablename__ = "search_runs"

    id: Mapped[int] = mapped_column(primary_key=True)
    datetime: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), index=True)
    news_count: Mapped[int] = mapped_column(Integer)

    # один запуск -> много новостей
    news_items: Mapped[list["News"]] = relationship(
        back_populates="run",
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<SearchRuns(id={self.id}, datetime='{self.datetime}', news_count='{self.news_count}')>"


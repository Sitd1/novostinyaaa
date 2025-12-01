from decimal import Decimal

from database.models.base import Base

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column


class Source(Base):
    __tablename__ = "source"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(255), index=True)
    name: Mapped[str] = mapped_column(String(32), index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    external_id: Mapped[str | None] = mapped_column(String(50), index=True)
    description: Mapped[str | None] = mapped_column(String(255), index=True)
    url: Mapped[str | None] = mapped_column(String(255), index=True)


class RawNewsORM(Base):
    # ToDo - переписать как в domain
    __tablename__ = "tg_raw_news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Идентификатор сообщения внутри канала / source
    external_id: Mapped[int] = mapped_column(Integer, index=True)

    # Дата и время публикации
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    # Дата получения, по умолчанию now()
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    # Текст сообщения (без медиа)
    text: Mapped[Optional[str]] = mapped_column(nullable=True)

    # Ссылка на саму новость
    url: Mapped[Optional[str]] = mapped_column(nullable=True)

    # Значения, которые будут считаться и обновляться

    # tags (скорее набор из нескольких значений)
    tags: Mapped[str] = mapped_column(nullable=True)
    importance: Mapped[Decimal] = mapped_column(nullable=True)
    summary: Mapped[str] = mapped_column(nullable=True)

    source_id: Mapped[str]  # ToDo foreign key

    # Можно добавить ещё поля (link, views, etc.)

    __table_args__ = (
        UniqueConstraint( "channel_username", "message_id", name="uq_channel_message"),
    )

    def __repr__(self) -> str:
        return f"<TgMessage channel={self.channel_username} msg_id={self.message_id}> pulished_at={self.published_at}>"

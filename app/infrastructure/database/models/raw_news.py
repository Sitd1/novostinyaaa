from database.models.base import Base


# models.py
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column



class RawNewsORM(Base):
    # ToDo - переписать как в domain
    __tablename__ = "tg_raw_news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Идентификатор канала
    # channel_id: Mapped[int] = mapped_column(BigInteger, index=True)
    channel_username: Mapped[Optional[str]] = mapped_column(String(255), index=True, nullable=True)

    # Идентификатор сообщения внутри канала
    message_id: Mapped[int] = mapped_column(Integer, index=True)

    # Дата сообщения
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    # Текст сообщения (без медиа)
    text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Можно добавить ещё поля (link, views, etc.)

    __table_args__ = (
        UniqueConstraint( "channel_username", "message_id", name="uq_channel_message"),
    )

    def __repr__(self) -> str:
        return f"<TgMessage channel={self.channel_username} msg_id={self.message_id}>"

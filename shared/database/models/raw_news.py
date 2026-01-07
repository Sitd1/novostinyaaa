from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, UniqueConstraint, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.database.models.base import Base



class RawNewsORM(Base):
    __tablename__ = "raw_news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Идентификатор сообщения внутри канала / source
    external_id: Mapped[str] = mapped_column(index=True)

    # Дата и время публикации
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    # Дата получения, по умолчанию now()
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        index=True,
        nullable=False,
        server_default=func.now(),
    )

    # Текст сообщения (без медиа)
    text: Mapped[str | None] = mapped_column(nullable=True)

    # Ссылка на саму новость
    url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # --- Значения, которые будут считаться и обновляться
    # Вариант: tags храним JSON (лучше всего) - должно быть несколько значений
    tags: Mapped[str | None] = mapped_column(Text, nullable=True)
    importance: Mapped[int] = mapped_column(Integer, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_payload: Mapped[str | None] = mapped_column(Text, nullable=True)  # весь сырой json, если есть

    # foreign key
    source_fk: Mapped[int] = mapped_column(ForeignKey("source.id"), index=True)
    # RawNewsORM
    event_id: Mapped[int | None] = mapped_column(ForeignKey("news_events.id"), index=True, nullable=True)

    # ORM связь
    source: Mapped["NewsSourceORM"] = relationship(back_populates="raw_news")
    event: Mapped["NewsEventORM"] = relationship(back_populates="raw_news")

    # связь many-to-many через junction table
    event_links: Mapped[list["NewsEventRawNewsORM"]] = relationship(
        back_populates="raw_news",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        UniqueConstraint("source_fk", "external_id", name="uq_source_msg"),
    )

    def __repr__(self) -> str:
        return f"<RawNews id={self.id} src={self.source_fk} ext_id={self.external_id}>"

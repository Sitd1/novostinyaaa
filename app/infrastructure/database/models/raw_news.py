from decimal import Decimal

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, UniqueConstraint, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.models.base import Base


class SourceORM(Base):
    """Таблица справочник для хранения источников новостей, значения должны быть уникальными"""
    __tablename__ = "source"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(255), index=True)
    name: Mapped[str] = mapped_column(String(32), index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    external_id: Mapped[str | None] = mapped_column(String(50), index=True)
    description: Mapped[str | None] = mapped_column(String(255), index=True)
    url: Mapped[str | None] = mapped_column(String(255), index=True)

    # связь 1 → N
    raw_news: Mapped[list["RawNewsORM"]] = relationship(
        back_populates="source", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<src_name={self.name} src_title={self.title}> description={self.description}>"



class RawNewsORM(Base):
    __tablename__ = "tg_raw_news"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Идентификатор сообщения внутри канала / source
    external_id: Mapped[int] = mapped_column(Integer, index=True)

    # Дата и время публикации
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    # Дата получения, по умолчанию now()
    fetched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)

    # Текст сообщения (без медиа)
    text: Mapped[str | None] = mapped_column(nullable=True)

    # Ссылка на саму новость
    url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Значения, которые будут считаться и обновляться

    # Вариант: tags храним JSON (лучше всего) - должно быть несколько значений
    tags: Mapped[str | None] = mapped_column(Text, nullable=True)
    importance: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=True)
    summary: Mapped[str] = mapped_column(Text, nullable=True)

    # foreign key
    source_fk: Mapped[int] = mapped_column(ForeignKey("source.id"), index=True)

    # ORM связь
    source: Mapped[SourceORM] = relationship(back_populates="raw_news")

    __table_args__ = (
        UniqueConstraint("source_fk", "external_id", name="uq_source_msg"),
    )

    def __repr__(self) -> str:
        return f"<RawNews id={self.id} src={self.source_fk} ext_id={self.external_id}>"

# app/infrastructure/database/repositories/raw_news_mapper.py
from app.core.domain.raw_news.entities import RawNews
from app.core.domain.sources.value_objects import SourceId, Url
from app.core.domain.raw_news.value_objects import (
    RawNewsId, ExternalMessageId, RawPublishedAt, RawFetchedAt,
    RawNewsText, RawPayload, Tag, RawNewsImportance,
    RawNewsSummary, RawNewsEmbedding, EventKey
)
from app.infrastructure.database.models.raw_news import RawNewsORM
from app.core.application.raw_news.dto.external_raw_news_item import ExternalRawNewsItem


class RawNewsMapper:
    @staticmethod
    def from_orm(orm_obj: RawNewsORM) -> RawNews:
        """Преобразование ORM-модели в доменную модель"""
        return RawNews(
            id=RawNewsId(orm_obj.id),
            source_id=SourceId(orm_obj.source_fk),
            external_id=ExternalMessageId(orm_obj.external_id) if orm_obj.external_id else None,
            published_at=RawPublishedAt(orm_obj.published_at),
            fetched_at=RawFetchedAt(orm_obj.fetched_at),
            text=RawNewsText(orm_obj.text) if orm_obj.text else None,
            url=Url(orm_obj.url) if orm_obj.url else None,
            raw_payload=RawPayload(orm_obj.raw_payload),
            tags=None,  # ToDo добавить обработку тэгов
            importance=RawNewsImportance(orm_obj.importance) if orm_obj.importance else None,
            summary=RawNewsSummary(orm_obj.summary) if orm_obj.summary else None,
            embedding=None,  # ToDo добавить embeddings в бд
            event_fk=EventKey(orm_obj.event_id) if orm_obj.event_id else None,
        )

    # @staticmethod
    # def to_orm(domain_obj: RawNews) -> dict:
    #     return ...
    # @staticmethod
    # def from_dto(dto: ExternalRawNewsItem) -> RawNews: ...
    #
    # @staticmethod
    # def update_orm(orm_obj: RawNewsORM, domain_obj: RawNews) -> None: ...
    #
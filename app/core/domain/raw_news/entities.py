from dataclasses import dataclass, replace

from app.core.domain.raw_news.value_objects import (
    RawNewsId,
    ExternalMessageId,
    RawPublishedAt,
    RawFetchedAt,

    Tag,
    RawNewsImportance,
    RawNewsText,
    RawNewsSummary,
    RawPayload, RawNewsEmbedding,
)
from app.core.domain.sources.value_objects import SourceId, Url


@dataclass(frozen=True)
class RawNews:
    id: RawNewsId
    source_id: SourceId
    external_id: ExternalMessageId | None  # id сообщения в TG / API
    published_at: RawPublishedAt    # когда опубликовали
    fetched_at: RawFetchedAt        # когда спарсили
    text: RawNewsText               # текст сообщения
    url: Url | None                 # ссылка на саму новость
    raw_payload: RawPayload         # весь сырой json, если есть

    # заполняются после постобработки
    tags: tuple[Tag, ...] | None = None
    importance: RawNewsImportance | None = None
    summary: RawNewsSummary | None = None
    embedding: RawNewsEmbedding | None = None

    def __post_init__(self):
        # Простейший инвариант: не может быть "получено" раньше, чем опубликовано
        if self.fetched_at.value < self.published_at.value:
            raise ValueError(
                f"RawNews: fetched_at {self.fetched_at} < published_at {self.published_at}"
            )

    # Доменные операции постобработки:

    def with_tags(self, tags: tuple[Tag, ...]) -> "RawNews":
        return replace(self, tags=tags)

    def with_summary(self, summary: RawNewsSummary) -> "RawNews":
        return replace(self, summary=summary)

    def with_importance(self, importance: RawNewsImportance) -> "RawNews":
        return replace(self, importance=importance)

    def with_embedding(self, embedding: RawNewsEmbedding) -> "RawNews":
        return replace(self, embedding=embedding)

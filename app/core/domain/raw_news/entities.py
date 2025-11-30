from dataclasses import dataclass

from app.core.domain.raw_news.value_objects import (
    RawNewsId,
    ExternalMessageId,
    Url,
    RawPublishedAt,
    RawFetchedAt,
    RawNewsText,
    Source,

    Tag,
    RawNewsImportance,
    RawNewsText,
    RawNewsSummary
)



@dataclass(frozen=True)
class RawNews:
    id: RawNewsId
    source: Source
    external_id: ExternalMessageId  # id сообщения в TG / API
    published_at: RawPublishedAt  # когда опубликовали
    fetched_at: RawFetchedAt  # когда спарсили
    text: RawNewsText  # сырой текст
    url: Url | None
    raw_payload: RawPayload  # весь сырой json, если есть

    # заполняются после постобработки
    tags: tuple[Tag, ...] | None = None
    interest_importance: RawNewsImportance | None = None
    summary: RawNewsSummary | None = None

    def __post_init__(self):
        # Простейший инвариант: не может быть "получено" раньше, чем опубликовано
        if self.fetched_at.value < self.published_at.value:
            raise ValueError(
                f"RawNews: fetched_at {self.fetched_at} < published_at {self.published_at}"
            )

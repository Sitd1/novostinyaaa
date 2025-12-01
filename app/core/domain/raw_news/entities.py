from dataclasses import dataclass, replace

from app.core.domain.raw_news.value_objects import (
    RawNewsId,
    ExternalMessageId,
    Url,
    RawPublishedAt,
    RawFetchedAt,

    Tag,
    RawNewsImportance,
    RawNewsText,
    RawNewsSummary,
    RawPayload,

    SourceId,
    SourceType,
    SourceName,
    SourceTitle,
    SourceDescription,
    ExternalSourceId,

    TgSourceName,
)


@dataclass(frozen=True)
class Source:
    id: SourceId | None            # auto-increment in DB
    type: SourceType               # enum: TELEGRAM, RSS, API, OTHER
    name: SourceName               # username: "meduza_tg_main"
    title: SourceTitle             # display name: "Meduza"
    external_id: ExternalSourceId | None = None
    description: SourceDescription | None = None
    url: Url | None = None

    @classmethod
    def telegram(
        cls,
        username: str,
        title: str,
        channel_code: str | None = None,
        url: str | None = None,
        description: str | None = None,
    ) -> "Source":

        return cls(
            id=None,
            type=SourceType.TELEGRAM,
            name=TgSourceName(username),
            title=SourceTitle(title),
            external_id=ExternalSourceId(channel_code) if channel_code else None,
            description=SourceDescription(description) if description else None,
            url=Url(url) if url else None,
        )


@dataclass(frozen=True)
class RawNews:
    id: RawNewsId
    source_id: SourceId
    external_id: ExternalMessageId  # id сообщения в TG / API
    published_at: RawPublishedAt    # когда опубликовали
    fetched_at: RawFetchedAt        # когда спарсили
    text: RawNewsText               # сырой текст
    url: Url | None
    raw_payload: RawPayload         # весь сырой json, если есть

    # заполняются после постобработки
    tags: tuple[Tag, ...] | None = None
    importance: RawNewsImportance | None = None
    summary: RawNewsSummary | None = None

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

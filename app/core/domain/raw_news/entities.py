from datetime import datetime
from dataclasses import dataclass

from app.core.domain.raw_news.value_objects import RawNewsId, SourceType, ExternalMessageId, Url, SourceTitle, \
    SourceName, SourceInternalCode, SourceDescription, RawPublishedAt, RawFetchedAt, RawNewsText


@dataclass(frozen=True)
class Source:
    type: SourceType    # enum: TELEGRAM, RSS, API, OTHER
    title: SourceTitle
    name: SourceName           # "Meduza", "The Bell" и т.д. tg channel name
    internal_code: SourceInternalCode | None # "meduza_tg_main" @lentach
    description: SourceDescription | None = None
    url: Url | None = None

    @classmethod
    def telegram(cls, name: str, channel_code: str, url: str | None = None, description: str | None = None) -> "Source":
        """
        channel_code — то, что тебе удобно:
        - username: "meduzalive"
        - или id: "123456789"
        """
        return cls(
            type=SourceType.TELEGRAM,
            name=name,
            internal_code=f"tg:{channel_code}",
            description=description,
            url=Url(url) if url else None,
        )




@dataclass
class RawNews:
    id: RawNewsId
    source: Source
    external_id: ExternalMessageId  # id сообщения в TG / API
    published_at: RawPublishedAt  # когда опубликовали
    fetched_at: RawFetchedAt  # когда спарсили
    text: RawNewsText  # сырой текст
    url: Url | None
    raw_payload: dict | None  # весь сырой json, если есть

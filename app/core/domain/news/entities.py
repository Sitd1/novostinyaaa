from datetime import datetime
from dataclasses import dataclass

from app.core.domain.news.value_objects import RawNewsId, Source, ExternalMessageId, Url


class RawNews:
    id: RawNewsId
    source: Source
    external_id: ExternalMessageId  # id сообщения в TG / API
    published_at: datetime
    fetched_at: datetime  # когда спарсили
    text: str
    url: Url | None
    raw_payload: dict | None  # весь сырой json, если есть

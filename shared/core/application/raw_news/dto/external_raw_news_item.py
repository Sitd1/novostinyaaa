from dataclasses import dataclass


@dataclass(frozen=True)
class ExternalRawNewsItem:
    """
    Входные сырые данные от источника.
    Это не доменная сущность, а просто транспортный объект.
    """
    external_id: str
    source: str
    text: str
    published_at: str  # или datetime, если ты уже конвертируешь

from enum import Enum
from urllib.parse import urlparse


class NewsEventId:
    value: int

class Title:
    value: str

class Summary:
    value: str  # уже очищенный/суммаризованный текст

class ImportanceLevel(Enum):
    CRITICAL = "critical"   # влияет на безопасность, большие деньги, рынок
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    IGNORE = "ignore"       # для внутренней пометки

class Topic(Enum):
    ECONOMY = "economy"
    POLITICS = "politics"
    TECHNOLOGY = "technology"
    SECURITY = "security"
    SOCIETY = "society"
    MARKET = "market"
    OTHER = "other"

class Tag:
    value: str  # более свободные метки: "санкции", "нефть", "AI", "выборы"

class Geography:
    country: str | None
    region: str | None
    city: str | None

class EventTime:
    # например, событие могло начаться вчера и длится сейчас
    started_at: datetime
    ended_at: datetime | None


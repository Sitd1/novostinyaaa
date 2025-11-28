from datetime import datetime
from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class NewsEventId:
    value: int

@dataclass(frozen=True)
class Title:
    value: str

@dataclass(frozen=True)
class Summary:
    value: str  # уже очищенный/суммаризованный текст

@dataclass(frozen=True)
class ImportanceLevel(Enum):
    CRITICAL = "critical"   # влияет на безопасность, большие деньги, рынок
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    IGNORE = "ignore"       # для внутренней пометки

@dataclass(frozen=True)
class Topic(Enum):
    ECONOMY = "economy"
    POLITICS = "politics"
    TECHNOLOGY = "technology"
    SECURITY = "security"
    SOCIETY = "society"
    MARKET = "market"
    OTHER = "other"


@dataclass(frozen=True)
class Geography:
    country: str | None
    region: str | None
    city: str | None

@dataclass(frozen=True)
class EventTime:
    # например, событие могло начаться вчера и длится сейчас
    started_at: datetime
    ended_at: datetime | None


@dataclass(frozen=True)
class UserInterestScore:
    value: int

@dataclass(frozen=True)
class Tag:
    value: str | None = None # более свободные метки: "санкции", "нефть", "AI", "выборы"

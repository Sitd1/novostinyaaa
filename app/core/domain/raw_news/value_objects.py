from dataclasses import dataclass
from datetime import datetime


# --- Основные VO для RawNews
@dataclass(frozen=True)
class RawNewsId:
    value: int


@dataclass(frozen=True)
class RawPublishedAt:
    value: datetime


@dataclass(frozen=True)
class RawFetchedAt:
    value: datetime


@dataclass(frozen=True)
class RawNewsText:
    value: str


@dataclass(frozen=True)
class ExternalMessageId:
    value: str | None  # msg_id в TG, guid в RSS и т.д.


@dataclass(frozen=True)
class RawPayload:
    value: dict | None

# --- VO, которые будут внесены после обработки RawNews

@dataclass(frozen=True)
class Tag:
    value: str | None = None # более свободные метки: "санкции", "нефть", "AI", "выборы"


@dataclass(frozen=True)
class RawNewsSummary:
    value: int | None = None


@dataclass(frozen=True)
class RawNewsImportance:
    value: float

    def __ge__(self, other: "RawNewsImportance") -> bool:
        return self.value >= other.value


@dataclass(frozen=True)
class RawNewsEmbedding:
    value: int | None = None

from datetime import datetime
from enum import Enum
from dataclasses import dataclass
from urllib.parse import urlparse

# --- Основные VO для RawNews
@dataclass(frozen=True)
class RawNewsId:
    value: int


@dataclass(frozen=True)
class SourceDescription:
    """Описание канала - можно добавлять, можно не добавлять"""
    value: str | None


@dataclass(frozen=True)
class RawPublishedAt:
    value: datetime


@dataclass(frozen=True)
class RawFetchedAt:
    value: datetime


@dataclass(frozen=True)
class RawNewsText:
    value: str


class SourceType(Enum):
    TELEGRAM = "telegram"
    # RSS = "rss"
    # API = "api"
    # OTHER = "other"


@dataclass(frozen=True)
class ExternalMessageId:
    value: str | None  # msg_id в TG, guid в RSS и т.д.


@dataclass(frozen=True)
class Url:
    value: str

    def __post_init__(self):
        parsed = urlparse(self.value)

        # Базовая валидация: протокол + домен
        if not parsed.scheme:
            raise ValueError(f"Url: missing scheme (http/https): '{self.value}'")

        if parsed.scheme not in ("http", "https"):
            raise ValueError(f"Url: unsupported scheme '{parsed.scheme}' in '{self.value}'")

        if not parsed.netloc:
            raise ValueError(f"Url: missing domain part in '{self.value}'")

        # Можно добавить простой check для домена
        if "." not in parsed.netloc:
            raise ValueError(f"Url: invalid domain '{parsed.netloc}' in '{self.value}'")


@dataclass(frozen=True)
class SourceTitle:
    """Человеческое название канала (как в канале)"""
    value: str


@dataclass(frozen=True)
class SourceName:
    """Для телеграма - это название канала @lentach"""
    value: str


@dataclass(frozen=True)
class SourceInternalCode:
    """Код канала (если есть) id12345"""
    value: str | None


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


# --- VO, которые будут внесены после обработки RawNews

@dataclass(frozen=True)
class Tag:
    value: str | None = None # более свободные метки: "санкции", "нефть", "AI", "выборы"

@dataclass(frozen=True)
class RawNewsSummary:
    value: int | None = None

@dataclass(frozen=True)
class RawNewsImportance(Enum):
    CRITICAL = "critical"   # влияет на безопасность, большие деньги, рынок
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    IGNORE = "ignore"       # для внутренней пометки

@dataclass(frozen=True)
class RawPayload:
    value: dict | None

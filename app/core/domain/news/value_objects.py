from enum import Enum
from dataclasses import dataclass
from urllib.parse import urlparse


@dataclass(frozen=True)
class RawNewsId:
    value: int


class SourceType(Enum):
    TELEGRAM = "telegram"
    RSS = "rss"
    API = "api"
    OTHER = "other"


@dataclass(frozen=True)
class Source:
    # пример: telegram channel, rss feed, api provider
    type: SourceType    # enum: TELEGRAM, RSS, API, OTHER
    name: str           # "Meduza", "The Bell" и т.д.
    internal_code: str  # "meduza_tg_main"


@dataclass(frozen=True)
class ExternalMessageId:
    value: str  # msg_id в TG, guid в RSS и т.д.


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


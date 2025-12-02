import re
from dataclasses import dataclass
from enum import Enum


# --- Source VO
@dataclass(frozen=True)
class SourceId:
    value: int


class SourceType(Enum):
    TELEGRAM = "telegram"
    # RSS = "rss"
    # API = "api"
    # OTHER = "other"


@dataclass(frozen=True)
class SourceName:
    """Для телеграма - это название канала @lentach"""
    value: str


@dataclass(frozen=True)
class SourceTitle:
    """Человеческое название канала (как в канале)"""
    value: str


@dataclass(frozen=True)
class ExternalSourceId:
    value: str


@dataclass(frozen=True)
class SourceDescription:
    """Описание канала - можно добавлять, можно не добавлять"""
    value: str | None


@dataclass(frozen=True)
class SourceName:
    """Для телеграма - это название канала @lentach"""
    value: str


@dataclass(frozen=True)
class TgSourceName(SourceName):
    value: str

    def __post_init__(self) -> None:
        v = self.value

        if not isinstance(v, str):
            raise TypeError("TgSourceName.value must be a string")

        # Разрешаем передавать с @, но внутри храним без @
        if v.startswith("@"):
            v = v[1:]

        # Нормализуем к нижнему регистру
        v = v.lower()

        # 1. Длина от 5 до 32 символов
        if not (5 <= len(v) <= 32):
            raise ValueError("TgSourceName must be between 5 and 32 characters")

        # 2. Только латинские буквы, цифры и подчёркивания
        if not re.fullmatch(r"[a-z0-9_]+", v):
            raise ValueError(
                "TgSourceName may contain only [a-z], digits [0-9] and underscore (_)"
            )

        # 3. Не должно начинаться с цифры
        if v[0].isdigit():
            raise ValueError("TgSourceName must not start with a digit")

        # 4. Нельзя использовать два подчёркивания подряд
        if "__" in v:
            raise ValueError("TgSourceName must not contain double underscores '__'")

        # 5. Нельзя заканчиваться на подчёркивание
        if v.endswith("_"):
            raise ValueError("TgSourceName must not end with underscore")

        # Так как dataclass(frozen=True), обновляем нормализованное значение через object.__setattr__
        object.__setattr__(self, "value", v)

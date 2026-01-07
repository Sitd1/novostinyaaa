from dataclasses import dataclass



@dataclass(frozen=True)
class UserId:
    value: int


@dataclass(frozen=True)
class HumanName:
    first: str
    last: str | None


@dataclass(frozen=True)
class TgUserName:
    """Username Telegram без символа @.
    В тг обычно обрашаются через @, напр. @sitd1"""
    value: str

@dataclass(frozen=True)
class TelegramId:
    value: int

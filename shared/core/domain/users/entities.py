from dataclasses import dataclass
from datetime import datetime

from value_objects import UserId, HumanName, TgUserName, TelegramId



@dataclass(frozen=True)
class TelegramUser:
    """
    Доменная сущность пользователя Telegram.
    """
    id: UserId
    name: HumanName  # То, что пишется в профиле
    username: TgUserName | None  # Никнейм
    telegram_id: TelegramId  # уникальный идентификатор Telegram
    created_at: datetime
    updated_at: datetime

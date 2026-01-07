# app/core/domain/users/factories.py
from datetime import datetime, timezone

from entities import TelegramUser
from value_objects import (
    UserId,
    HumanName,
    TgUserName,
    TelegramId,
)


class TelegramUserFactory:
    """
    Фабрика для создания доменной сущности TelegramUser.
    Не знает про БД, только про доменные объекты.
    """

    @staticmethod
    def create_new(
        *,
        user_id: UserId,
        telegram_id: TelegramId,
        name: HumanName,
        username: TgUserName | None,
        now: datetime | None = None,
    ) -> TelegramUser:
        """
        Создать нового пользователя Telegram с корректно выставленными датами.
        """
        ts = now or datetime.now(timezone.utc)

        return TelegramUser(
            id=user_id,
            name=name,
            username=username,
            telegram_id=telegram_id,
            created_at=ts,
            updated_at=ts,
        )

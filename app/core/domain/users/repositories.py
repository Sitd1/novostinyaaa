from typing import Protocol

from app.core.domain.users.entities import TelegramUser
from app.core.domain.users.value_objects import UserId, TelegramId


class TelegramUserRepository(Protocol):
    """
    Доменный интерфейс (порт) для работы с пользователями Telegram.
    Инфраструктура (БД, ORM и т.п.) реализует этот протокол.
    """

    async def get_by_id(self, user_id: UserId) -> TelegramUser | None:
        """Найти пользователя по нашему внутреннему ID."""
        ...

    async def get_by_telegram_id(self, telegram_id: TelegramId) -> TelegramUser | None:
        """Найти пользователя по Telegram ID (главный внешний идентификатор)."""
        ...

    async def save(self, user: TelegramUser) -> None:
        """
        Сохранить (insert/update) пользователя.
        Детали upsert-логики — уже в конкретной реализации.
        """
        ...

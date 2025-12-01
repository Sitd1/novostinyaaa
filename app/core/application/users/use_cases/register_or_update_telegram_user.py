# app/core/application/users/use_cases/register_or_update_telegram_user.py

from dataclasses import replace
from datetime import datetime, timezone

from app.core.domain.users.entities import TelegramUser
from app.core.domain.users.factories import TelegramUserFactory
from app.core.domain.users.repositories import TelegramUserRepository
from app.core.domain.users.value_objects import (
    HumanName,
    TgUserName,
    TelegramId,
    UserId,
)


async def register_or_update_telegram_user(
    *,
    repo: TelegramUserRepository,
    factory: TelegramUserFactory,
    telegram_id: TelegramId,
    name: HumanName,
    username: TgUserName | None,
    user_id: UserId | None = None,
    now: datetime | None = None,
) -> TelegramUser:
    """
    Юз-кейс: зарегистрировать нового или обновить существующего пользователя Telegram.

    - ищет пользователя по telegram_id
    - если не найден -> создаёт нового через фабрику
    - если найден -> обновляет профиль (name, username, updated_at)
    """
    ts = now or datetime.now(timezone.utc)

    existing = await repo.get_by_telegram_id(telegram_id)

    if existing is None:
        # Если user_id не передали — тут обычно генерируется новый id
        if user_id is None:
            raise ValueError("user_id must be provided for new TelegramUser")

        user = factory.create_new(
            user_id=user_id,
            telegram_id=telegram_id,
            name=name,
            username=username,
            now=ts,
        )
        await repo.save(user)
        return user

    # Обновляем существующего пользователя
    updated_user = replace(
        existing,
        name=name,
        username=username,
        updated_at=ts,
    )
    await repo.save(updated_user)
    return updated_user

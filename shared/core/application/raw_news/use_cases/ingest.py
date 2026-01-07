# Шаг 1
# --- ingest - процесс получения "сырого" внешнего входа → преобразования → сохранения в хранилище.
# 1. Приём сырых новостей из внешнего источника
# IngestRawNewsBatch
# Вход: список сообщений из Telegram/других источников
# Действия: создать RawNews для каждого, сохранить в репозиторий, отфильтровать дубли по внешнему id
# Выход: список новых RawNews, которые попали в систему

from __future__ import annotations

from external_raw_news_item import ExternalRawNewsItem
from ingest import ExternalRawNewsSource
from entities import RawNews
from repositories import RawNewsRepository
from services import RawNewsFactory


async def fetch_new_raw_news(
    source: ExternalRawNewsSource,
) -> list[ExternalRawNewsItem]:
    """
    Забрать новые сырые сообщения из внешнего источника в виде DTO.
    Это ещё НЕ доменные сущности, просто транспортный слой.
    (по сути не нужен, только для теста)
    """
    items = [item async for item in source.fetch_new_raw_items()]
    return items


async def ingest_new_raw_news(
    source: ExternalRawNewsSource,
    factory: RawNewsFactory,
    repo: RawNewsRepository,
) -> int:
    """
    Основной use-case:
    1. Забирает новые raw news из внешнего источника (порт)
    2. Превращает DTO в доменные RawNews (фабрика)
    3. Сохраняет доменные RawNews пачкой через репозиторий
    """
    # 1. Получили DTO
    raw_items = [item async for item in source.fetch_new_raw_items()]

    # 2. Превратили в доменные сущности
    raw_news_list: list[RawNews] = [
        factory.create_from_external_item(raw_news_) for raw_news_ in raw_items
    ]
    created_count = len(raw_news_list)

    # 3. Сохранили пачкой
    await repo.save_many(raw_news_list)

    return created_count

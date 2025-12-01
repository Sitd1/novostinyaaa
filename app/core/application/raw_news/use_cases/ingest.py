# Шаг 1
# --- ingest - процесс получения "сырого" внешнего входа → преобразования → сохранения в хранилище.
# 1. Приём сырых новостей из внешнего источника
# IngestRawNewsBatch
# Вход: список сообщений из Telegram/других источников
# Действия: создать RawNews для каждого, сохранить в репозиторий, отфильтровать дубли по внешнему id
# Выход: список новых RawNews, которые попали в систему

from __future__ import annotations

from typing import Iterable, Sequence

from app.core.domain.raw_news.entities import RawNews
from app.core.application.raw_news.dto.external_raw_news_item import ExternalRawNewsItem
from app.core.application.raw_news.ports.ingest import ExternalRawNewsSource
from app.core.domain.raw_news.repositories import RawNewsRepository
from app.core.domain.raw_news.services import RawNewsFactory


async def fetch_new_raw_news(
    source: ExternalRawNewsSource,
) -> list[ExternalRawNewsItem]:
    items = [item async for item in source.fetch_new_raw_items()]
    return items


async def deduplicate_raw_news(
    items: Iterable[ExternalRawNewsItem],
    repo: RawNewsRepository,
) -> list[ExternalRawNewsItem]:
    unique: list[ExternalRawNewsItem] = []
    for item in items:
        exists = await repo.exists_by_external_id(item.external_id)
        if not exists:
            unique.append(item)
    return unique


async def store_raw_news(
    items: Iterable[ExternalRawNewsItem],
    repo: RawNewsRepository,
    factory: RawNewsFactory,
) -> list[RawNews]:
    raw_news_list: list[RawNews] = [factory.create_from_external(item) for item in items]
    await repo.save_many(raw_news_list)
    return raw_news_list

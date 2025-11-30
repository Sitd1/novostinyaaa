# Шаг 1
# --- ingest - процесс получения "сырого" внешнего входа → преобразования → сохранения в хранилище.
# 1. Приём сырых новостей из внешнего источника
# IngestRawNewsBatch
# Вход: список сообщений из Telegram/других источников
# Действия: создать RawNews для каждого, сохранить в репозиторий, отфильтровать дубли по внешнему id
# Выход: список новых RawNews, которые попали в систему

from __future__ import annotations

from typing import Protocol, Iterable, Sequence

from app.core.domain.raw_news.entities import RawNews
from app.core.application.raw_news.dto.external_raw_news_item import ExternalRawNewsItem


class ExternalRawNewsSource(Protocol):
    """
    Порт для источника сырых новостей (Telegram, RSS, API и т.п.).
    """

    async def fetch_new_raw_items(self) -> Iterable["ExternalRawNewsItem"]:
        """
        Получить новые сообщения из внешнего источника в «сыром» формате.
        Формат ExternalRawNewsItem – простой DTO, ещё не доменная сущность.
        """
        ...


class RawNewsRepository(Protocol):
    """
    Порт репозитория для RawNews (доменный слой).
    """

    async def exists_by_external_id(self, external_id: str) -> bool:
        ...

    async def save_many(self, items: Sequence[RawNews]) -> None:
        ...


async def fetch_new_raw_news(
    source: ExternalRawNewsSource,
) -> list[ExternalRawNewsItem]:
    """
    Use case:
    - получить новые сообщения из источника в виде ExternalRawNewsItem.
    """
    items = [item async for item in source.fetch_new_raw_items()]
    return items


async def deduplicate_raw_news(
    items: Iterable[ExternalRawNewsItem],
    repo: RawNewsRepository,
) -> list[ExternalRawNewsItem]:
    """
    Use case:
    - убрать дубли по external_id (и источнику, если нужно).
    - оставить только те, которых ещё нет в хранилище RawNews.
    """
    unique: list[ExternalRawNewsItem] = []

    for item in items:
        exists = await repo.exists_by_external_id(item.external_id)
        if not exists:
            unique.append(item)

    return unique


async def store_raw_news(
    items: Iterable[ExternalRawNewsItem],
    repo: RawNewsRepository,
    factory: "RawNewsFactory",
) -> list[RawNews]:
    """
    Use case:
    - сконвертировать ExternalRawNewsItem -> RawNews (через фабрику домена)
    - сохранить новые RawNews.
    """
    raw_news_list: list[RawNews] = [factory.create_from_external(item) for item in items]
    await repo.save_many(raw_news_list)
    return raw_news_list


class RawNewsFactory(Protocol):
    """
    Порт/фабрика домена для создания RawNews из входных данных.
    """

    def create_from_external(self, item: ExternalRawNewsItem) -> RawNews:
        ...

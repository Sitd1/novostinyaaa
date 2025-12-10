from __future__ import annotations

from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.repositories import RawNewsRepository


# 1. Use case для загрузки необработанных новостей
async def load_pending_raw_news_for_clustering(
        raw_repo: RawNewsRepository,
        limit: int | None = None) -> list[RawNews]:
    """Загружает новости, ожидающие кластеризации.
        1. `event_fk is None`
        2. `summary is not None`
        3. `embedding is not None`
    """
    return await raw_repo.list_pending_for_event_clustering(limit=limit)

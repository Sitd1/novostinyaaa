# Шаг 3
# 3. Фильтрация новостей
#     - Отфильтровываем по tags
#     - Фильтр по importance
from __future__ import annotations

from typing import Iterable, Sequence

from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.value_objects import RawNewsImportance, Tag
from app.core.domain.raw_news.repositories import RawNewsRepository


async def get_filtered_raw_news_by_tags(
    repo: RawNewsRepository,
    required_tags: Sequence[Tag],
    importance_threshold: RawNewsImportance,
    limit: int | None = None
) -> list[RawNews]:

    """
        Query use case:
        - отфильтровать RawNews по нужным тегам и порогу важности
        - вернуть результат
        """
    return await repo.get_filtered_news(
        required_tags=required_tags,
        importance_threshold=importance_threshold,
        limit=limit
    )

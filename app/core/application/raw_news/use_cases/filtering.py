# Шаг 3
# 3. Фильтрация новостей
#     - Отфильтровываем по tags
#     - Фильтр по importance
from __future__ import annotations

from typing import Iterable, Sequence

from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.value_objects import RawNewsImportance, Tag


def filter_raw_news_by_tags(
    items: Iterable[RawNews],
    required_tags: Sequence[Tag],
) -> list[RawNews]:
    """
    Use case:
    - отфильтровать RawNews по наличию нужных тегов.
    """
    required = set(required_tags)
    result: list[RawNews] = []

    for item in items:
        item_tags = set(item.tags)  # предполагаем, что в сущности есть .tags
        if required.issubset(item_tags):
            result.append(item)

    return result


def filter_raw_news_by_importance(
    items: Iterable[RawNews],
    min_importance: RawNewsImportance,
) -> list[RawNews]:
    """
    Use case:
    - отфильтровать RawNews по числовому скору важности.
    """
    return [
        item
        for item in items
        if item.importance >= min_importance
    ]

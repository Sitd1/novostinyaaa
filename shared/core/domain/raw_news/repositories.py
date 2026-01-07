from __future__ import annotations

from typing import Protocol, Iterable

from entities import RawNews
from value_objects import (
    RawNewsId,
    RawNewsImportance, Tag,
)
from entities import NewsEvent


class RawNewsRepository(Protocol):
    async def get(self, id: RawNewsId) -> RawNews | None: ...
    async def list_pending_for_event_clustering(
            self,
            limit: int | None = None
    ) -> list[RawNews]: ...
    async def get_filtered_news(
            self,
            required_tags: Iterable[Tag],
            importance_threshold: RawNewsImportance,
            limit: int | None = None
    ) -> list[RawNews]: ...
    async def save_many(self, items: Iterable[RawNews]) -> None: ...
    async def update_many(self, items: Iterable[RawNews]) -> None: ...


class EventAgent(Protocol):
    async def set_news_event(self, raw_news, events_repo, candidates) -> NewsEvent: ...


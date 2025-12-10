from __future__ import annotations

from typing import Protocol, Iterable

from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.value_objects import (
    RawNewsId,
    RawNewsImportance, Tag,
)



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

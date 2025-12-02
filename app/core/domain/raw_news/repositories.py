from __future__ import annotations

from typing import Protocol, Iterable
from abc import abstractmethod

from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.value_objects import (
    RawNewsId,
    ExternalMessageId,
)
from app.core.domain.sources.entities import Source



class RawNewsRepository(Protocol):
    async def get(self, id: RawNewsId) -> RawNews | None: ...
    async def list_pending_for_processing(
            self,
            limit: int | None = None
    ) -> list[RawNews]: ...
    async def save_many(self, items: Iterable[RawNews]) -> None: ...
    async def update_many(self, items: Iterable[RawNews]) -> None: ...

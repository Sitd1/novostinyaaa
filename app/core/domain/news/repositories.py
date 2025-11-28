# Тут только абстракция
from abc import ABC, abstractmethod
from typing import Iterable, Optional

from app.core.domain.raw_news.value_objects import RawNewsId
from app.core.domain.news.entities import NewsEvent
from app.core.domain.news.value_objects import NewsEventId


class NewsEventRepository(ABC):
    """
    Domain-level repository interface for NewsEvent Aggregates.
    This layer knows only about domain model and business abstractions.
    No ORM/SQL/DTO.
    """

    @abstractmethod
    async def get_by_id(self, event_id: NewsEventId) -> Optional[NewsEvent]:
        """Return event by id or None."""
        raise NotImplementedError

    def find_by_raw_news_ids(
            self,
            raw_news_ids: list[RawNewsId],
    ) -> list[NewsEvent]:
        """
        Найти события, которые уже содержат указанные RawNewsID.

        Обычно реализуется через join-таблицу
        news_event_raw_news(event_id, raw_news_id)
        """
        ...

    @abstractmethod
    async def add(self, event: NewsEvent) -> None:
        """Store a new event."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, event: NewsEvent) -> None:
        """Persist changes to existing event."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, event_id: NewsEventId) -> None:
        """Delete event by id."""
        raise NotImplementedError

    @abstractmethod
    async def list_recent(self, limit: int = 50) -> Iterable[NewsEvent]:
        """Return last N events."""
        raise NotImplementedError

    @abstractmethod
    async def find_duplicates(self, event: NewsEvent) -> Iterable[NewsEvent]:
        """
        Domain-specific method.
        Used for deduplication logic (e.g. by title, time, content).
        """
        raise NotImplementedError

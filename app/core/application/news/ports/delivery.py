from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Iterable, Sequence

from app.core.domain.news.entities import NewsEvent
from app.core.domain.users.entities import User  # если есть такая сущность




class InterestScoringService(Protocol):
    async def score_for_user(
        self,
        user: User,
        event: NewsEvent,
    ) -> float:
        ...


class NewsDeliveryGateway(Protocol):
    async def deliver(self, user: User, events: Sequence[NewsEvent]) -> None:
        """
        Отправить подборку пользователю (бот, email, push и т.п.).
        """
        ...

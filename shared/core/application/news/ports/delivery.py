from __future__ import annotations

from typing import Protocol, Sequence

from entities import NewsEvent
from entities import User  # если есть такая сущность




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

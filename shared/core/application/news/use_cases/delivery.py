# Шаг 2
# Отправка сущности "новость"
# 6. Отправление пользователю
#     - Отобрать новости, подходящие пользователю
#     - Посчитать вероятную interest_score_for_user
#         - отфильтровать по threashold: interest_score_for_user, по тегам
#     - Отправить финальную подборку пользователю
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Iterable, Sequence

from entities import NewsEvent
from entities import User  # если есть такая сущность


@dataclass(frozen=True)
class ScoredNewsEvent:
    event: NewsEvent
    score: float


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


async def score_interest_for_user(
    user: User,
    events: Iterable[NewsEvent],
    scoring: InterestScoringService,
) -> list[ScoredNewsEvent]:
    """
    Use case:
    - посчитать interest_score_for_user для каждого события.
    """
    result: list[ScoredNewsEvent] = []

    for event in events:
        score = await scoring.score_for_user(user, event)
        result.append(ScoredNewsEvent(event=event, score=score))

    return result


def filter_events_for_user(
    scored_events: Iterable[ScoredNewsEvent],
    threshold: float,
    limit: int | None = None,
) -> list[NewsEvent]:
    """
    Use case:
    - отфильтровать события по порогу интереса.
    - опционально ограничить количество.
    """
    filtered = [se for se in scored_events if se.score >= threshold]
    # сортируем по убыванию интереса
    filtered.sort(key=lambda se: se.score, reverse=True)

    events_only = [se.event for se in filtered]
    if limit is not None:
        events_only = events_only[:limit]

    return events_only


async def deliver_news_events_to_user(
    user: User,
    events: Sequence[NewsEvent],
    delivery_gateway: NewsDeliveryGateway,
) -> None:
    """
    Use case:
    - отправить финальную подборку пользователю.
    """
    if not events:
        return

    await delivery_gateway.deliver(user, events)

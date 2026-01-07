from __future__ import annotations
from dataclasses import replace
from datetime import datetime
from typing import Iterable

from entities import RawNews
from value_objects import RawNewsId
from entities import NewsEvent
from value_objects import (
    NewsEventId,
    EventTime,
)
from repositories import NewsEventRepository
from ports import (
    SimilarRawNewsFinder,
    NewsSummarizer,
)


class NewsEventGrouperService:
    """
    Доменный сервис: определить, к какому событию относится RawNews.
    Если нет подходящего — создать новый NewsEvent.
    """

    def __init__(
        self,
        event_repo: NewsEventRepository,
        similar_finder: SimilarRawNewsFinder,
        summarizer: NewsSummarizer,
    ) -> None:
        self._events = event_repo
        self._similar = similar_finder
        self._summarizer = summarizer

    # --------------------------------------------------------

    def attach_raw_news(self, raw: RawNews) -> NewsEvent:
        """
        Основная операция:
        - ищем похожие сырые новости
        - ищем событие, куда они входят
        - либо обновляем существующее
        - либо создаём новое
        """

        similar_raw = self._similar.find_similar(raw)
        similar_ids = [r.id for r in similar_raw] + [raw.id]

        related_events = self._events.find_by_raw_news_ids(similar_ids)

        if related_events:
            event = self._choose_primary_event(related_events)
            updated = self._rebuild_event_with_added_raw(event, raw)
            self._events.save(updated)
            return updated

        # создаём новое
        new_event = self._build_new_event([raw] + similar_raw)
        self._events.add(new_event)
        return new_event

    # --------------------------------------------------------

    def _choose_primary_event(self, events: list[NewsEvent]) -> NewsEvent:
        """
        Самая простая стратегия — выбираем самое свежее событие.
        """
        return sorted(events, key=lambda e: e.created_at)[-1]

    def _rebuild_event_with_added_raw(
        self,
        event: NewsEvent,
        new_raw: RawNews,
    ) -> NewsEvent:
        """
        Добавить raw.id в список события и частично пересчитать summary/tags.
        """

        raw_ids: list[RawNewsId] = list(event.raw_news_ids) + [new_raw.id]

        summary = self._summarizer.make_summary([new_raw])
        new_tags = self._summarizer.infer_tags([new_raw])

        return replace(
            event,
            raw_news_ids=raw_ids,
            summary=summary,
            tags=event.tags + new_tags,
            updated_at=datetime.utcnow(),
        )

    def _build_new_event(
        self,
        items: Iterable[RawNews],
    ) -> NewsEvent:
        """
        Построение нового NewsEvent из пачки сырых новостей.
        """

        items = list(items)

        title = self._summarizer.make_title(items)
        summary = self._summarizer.make_summary(items)
        topics = self._summarizer.infer_topics(items)
        tags = self._summarizer.infer_tags(items)
        importance = self._summarizer.infer_importance(items)

        raw_ids = [i.id for i in items]
        now = datetime.utcnow()

        return NewsEvent(
            id=NewsEventId.new(),
            created_at=now,
            updated_at=now,
            raw_news_ids=raw_ids,
            title=title,
            summary=summary,
            importance=importance,
            topics=topics,
            tags=tags,
            geography=None,
            event_time=EventTime.from_raw_items(items),
        )


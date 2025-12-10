from datetime import timezone

from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime
from typing import Iterable

from app.core.domain.news.value_objects import (
    NewsEventId,
    Title,
    Summary,
    ImportanceLevel,
    # Topic,
    Tag,
    Geography,
    EventTime,
    UserInterestScore,
    Source,
)
from app.core.domain.raw_news.value_objects import RawNewsId


@dataclass(frozen=True)
class NewsEvent:
    """
    Агрегат "событие новости":
    - агрегирует сырые новости (raw_news_ids)
    - хранит нормализованный заголовок, summary, важность и т.д.
    """

    id: NewsEventId
    created_at: datetime
    updated_at: datetime

    # ГРУППА сырых новостей - связь с сырыми новостями (могут жить в инфраструктуре/ORM)
    raw_news_ids: tuple[RawNewsId, ...]
    # доменные поля
    title: Title

    summary: Summary               # расчетное поле
    importance: ImportanceLevel    # расчетное поле
    tags: tuple[Tag, ...]          # расчетное поле
    # topics: tuple[Topic, ...]      # расчетное поле
    geography: Geography | None    # расчетное поле

    sources: tuple[Source, ...]

    event_time: EventTime  # когда это произошло / актуально
    user_interest_score: UserInterestScore | None = None  # интересы отдельного пользователя
    is_updated: bool = False

    # ---------- Фабрики / конструкторы ----------

    @classmethod
    def create(
        cls,
        id: NewsEventId,
        title: Title,
        summary: Summary,
        importance: ImportanceLevel,
        event_time: EventTime,
        *,
        raw_news_ids: Iterable[RawNewsId] = (),
        tags: Iterable[Tag] = (),
        geography: Geography | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        user_interest_score: UserInterestScore | None = None,
        is_updated: bool = False,
    ) -> "NewsEvent":
        """
        Удобная фабрика: принимает обычные Iterable, внутри приводит к tuple.
        created_at / updated_at можно прокинуть снаружи (например, из БД),
        или выставить одинаково при создании.
            Принимает обычные итерабельные (list, set, и т.п.).
            Внутри приводит к tuple + убирает дубликаты через dict.fromkeys(...)
        """
        now = datetime.now(timezone.utc)
        created = created_at or now
        updated = updated_at or now

        # убираем дубликаты и фиксируем порядок
        raw_ids_tuple = tuple(dict.fromkeys(raw_news_ids))
        tags_tuple = tuple(dict.fromkeys(tags))

        return cls(
            id=id,
            created_at=created,
            updated_at=updated,
            raw_news_ids=raw_ids_tuple,
            title=title,
            summary=summary,
            importance=importance,
            tags=tags_tuple,
            geography=geography,
            event_time=event_time,
            user_interest_score=user_interest_score,
            is_updated=is_updated
        )

    # ---------- Методы поведения (immutability) ----------

    def with_added_raw_news(self, raw_id: RawNewsId) -> "NewsEvent":
        """
        Вернуть новый NewsEvent с добавленным raw_news_id.
        Не добавляет дубликат, если id уже есть.
        """
        if raw_id in self.raw_news_ids:
            return self

        new_raw_ids = self.raw_news_ids + (raw_id,)
        return replace(self, raw_news_ids=new_raw_ids)

    def with_removed_raw_news(self, raw_id: RawNewsId) -> "NewsEvent":
        """
        Вернуть новый NewsEvent без указанного raw_news_id.
        Если такого id нет — вернём self как есть.
        """
        if raw_id not in self.raw_news_ids:
            return self

        new_raw_ids = tuple(rid for rid in self.raw_news_ids if rid != raw_id)
        return replace(self, raw_news_ids=new_raw_ids)

    # def with_topics(self, topics: Iterable[Topic]) -> "NewsEvent":
    #     """
    #     Полностью заменить список topics.
    #     """
    #     topics_tuple = tuple(dict.fromkeys(topics))
    #     return replace(self, topics=topics_tuple)
    #
    # def with_added_topic(self, topic: Topic) -> "NewsEvent":
    #     """
    #     Добавить один Topic, без дубликатов.
    #     """
    #     if topic in self.topics:
    #         return self
    #
    #     new_topics = self.topics + (topic,)
    #     return replace(self, topics=new_topics)
    #
    # def with_removed_topic(self, topic: Topic) -> "NewsEvent":
    #     """
    #     Убрать один Topic.
    #     """
    #     if topic not in self.topics:
    #         return self
    #
    #     new_topics = tuple(t for t in self.topics if t != topic)
    #     return replace(self, topics=new_topics)

    def with_tags(self, tags: Iterable[Tag]) -> "NewsEvent":
        """
        Полностью заменить список tags.
        """
        tags_tuple = tuple(dict.fromkeys(tags))
        return replace(self, tags=tags_tuple)

    def with_added_tag(self, tag: Tag) -> "NewsEvent":
        """
        Добавить один Tag, без дубликатов.
        """
        if tag in self.tags:
            return self

        new_tags = self.tags + (tag,)
        return replace(self, tags=new_tags)

    def with_removed_tag(self, tag: Tag) -> "NewsEvent":
        """
        Убрать один Tag.
        """
        if tag not in self.tags:
            return self

        new_tags = tuple(t for t in self.tags if t != tag)
        return replace(self, tags=new_tags)

    def with_geography(self, geography: Geography | None) -> "NewsEvent":
        """
        Заменить Geography.
        """
        return replace(self, geography=geography)

    def with_importance(self, importance: ImportanceLevel) -> "NewsEvent":
        """
        Обновить ImportanceLevel.
        """
        return replace(self, importance=importance)

    def touch(self, *, at: datetime | None = None) -> "NewsEvent":
        """
        Обновить updated_at (например, при любом изменении).
        """
        return replace(
            self,
            updated_at=at or datetime.now(timezone.utc),
            is_updated=True)

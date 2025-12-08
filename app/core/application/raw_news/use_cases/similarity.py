# Шаг 4
# 4. Работа с векторами
#     - Найти похожие raw_news (по embedding)
#     - Объединить похожие raw_news в группы (кластеризация) ---->(как указать группы?)
# Работа с RawNews закончена
from __future__ import annotations

import asyncio
from datetime import timedelta

from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.repositories import (
    RawNewsRepository,
    NewsEventRepository,
    SimilarityMatcherService
)
from app.core.application.raw_news.config import ClusteringConfig
from app.core.domain.news.entities import NewsEvent
from models import raw_news


class RawNewsSimilarityUseCase:
    def __init__(
        self,
        raw_repo: RawNewsRepository,
        events_repo: NewsEventRepository,
        similarity_matcher: SimilarityMatcherService,
        config: ClusteringConfig | None = None,
        limit: int | None = None,
    ):
        self.raw_repo = raw_repo
        self.events_repo = events_repo
        self.similarity_matcher = similarity_matcher
        self.config = config if config is not None else ClusteringConfig()
        self.limit = limit

        self.executed_raw_news: list[RawNews] | None = None

        self.updated_raw_news: list[RawNews] = []
        self.new_events: list[NewsEvent] = []
        self.updated_events: list[NewsEvent] = []

    async def process_one_raw_news(self, raw: RawNews) -> None:
        """Ищем кандидаты-события - получить небольшой список событий,
                с которыми можно сравнить текущую новость.
                Смотрим ближайшие и косинусное расстояние отсеиваем по threshold также смотрим прочие фильтры
                """

        # совпадение по диапазону времени window_start, window_end и прочее по конфигу
        event_candidates = self.events_repo.get_news_events_candidates(raw, self.config)

        if event_candidates:
            similarity_candidates = await self.similarity_matcher.get_similar_news_candidates(
                raw, self.config
            )
        else:
            similarity_candidates = {}

        # Создание нового события (нет подходящих events)
        if not similarity_candidates:
            event = await self.events_repo.create_from_raw_news(raw)
            self.new_events.append(event)
        else:
            chosen_event = await self.similarity_matcher.similaritychoose_event_for_raw_news(
                raw, similarity_candidates
            )
            if chosen_event is None:
                event = await self.events_repo.create_from_raw_news(raw)
                self.new_events.append(event)
            else:
                event = await self.events_repo.attach_raw_to_existing_event(raw, chosen_event)
                self.updated_events.append(event)

        # обновляем только raw приписывая event_id в качестве fk
        raw = raw.with_event_key(event.id)
        self.updated_raw_news.append(raw)

    async def execute_raw_news(self) -> list[RawNews]:
        self.executed_raw_news = await self.raw_repo.list_pending_for_event_clustering(
            limit=self.limit
        )
        return self.executed_raw_news

    async def process_raw_news(self):
        # можно распараллелить (только если репозитории поддерживают многопоточность
        raw_list = await self.execute_raw_news()
        await asyncio.gather(*(self.process_one_raw_news(raw) for raw in raw_list))

    async def save_updates(self) -> None:
        await self.raw_repo.update_many(self.updated_raw_news)
        await self.events_repo.update_many(self.updated_events)
        await self.events_repo.save_many(self.new_events)


async def create_events_from_raw_news(
        raw_repo: RawNewsRepository,
        events_repo: NewsEventRepository,
        similarity_matcher: SimilarityMatcherService,
        config: ClusteringConfig | None = None,
        limit: int | None = None
) -> list[RawNews]:

    rns = RawNewsSimilarityUseCase(
        raw_repo=raw_repo,
        events_repo=events_repo,
        similarity_matcher=similarity_matcher,
        config=config,
        limit=limit
    )
    await rns.execute_raw_news()

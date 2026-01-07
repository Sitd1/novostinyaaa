# Шаг 4
# 4. Работа с векторами
#     - Найти похожие raw_news (по embedding)
#     - Объединить похожие raw_news в группы (кластеризация) ---->(как указать группы?)
# Работа с RawNews закончена
from __future__ import annotations

from application import ClusteringConfig
from entities import NewsEvent
from entities import RawNews
from repositories import (
    RawNewsRepository,
    NewsEventRepository,
    SimilarityMatcherService
)


class EventAggregationUseCase:
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
        """Обрабатывает одну сырую новость: ищет событие или создаёт новое."""

        event_candidates: list[NewsEvent] = self.events_repo.get_news_events_candidates(raw, self.config)

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

        # обновляем только raw, приписывая event_id в качестве fk
        raw = raw.with_event_key(event.id)
        self.updated_raw_news.append(raw)

    async def execute_raw_news(self) -> list[RawNews]:
        self.executed_raw_news = await self.raw_repo.list_pending_for_event_clustering(
            limit=self.limit
        )
        return self.executed_raw_news

    async def process_raw_news(self, raw_news_list: list[RawNews] | None = None) -> None:
        """Обработать список новостей. Если список не передан — загружаем сами."""
        if raw_news_list is None:
            raw_news_list = await self.execute_raw_news()

        for raw_news in raw_news_list:
            await self.process_one_raw_news(raw_news)

    async def save_updates(self) -> None:
        """Сохранить все накопленные изменения в репозитории."""
        if self.updated_raw_news:
            await self.raw_repo.update_many(self.updated_raw_news)

        if self.updated_events:
            await self.events_repo.update_many(self.updated_events)

        if self.new_events:
            await self.events_repo.save_many(self.new_events)

    async def execute(self) -> None:
        """Запускает весь пайплайн:
        1) загружаем сырые новости
        2) обрабатываем их
        3) сохраняем изменения
        """

        # на всякий случай чистим состояние, если use-case переиспользуют
        self.executed_raw_news = None
        self.updated_raw_news = []
        self.new_events = []
        self.updated_events = []

        await self.process_raw_news()
        await self.save_updates()


async def create_events_from_raw_news(
        raw_repo: RawNewsRepository,
        events_repo: NewsEventRepository,
        similarity_matcher: SimilarityMatcherService,
        config: ClusteringConfig | None = None,
        limit: int | None = None
) -> list[RawNews]:

    rns = EventAggregationUseCase(
        raw_repo=raw_repo,
        events_repo=events_repo,
        similarity_matcher=similarity_matcher,
        config=config,
        limit=limit
    )
    await rns.execute()


# ------------------------------------------------------------------------------------------
# ---
# ------------------------------------------------------------------------------------------




# 2. Use case для обработки одной новости
async def process_single_raw_news_for_event(
        raw_news: RawNews,
        events_repo: NewsEventRepository,
        similarity_matcher: SimilarityMatcherService,
        config: ClusteringConfig):
    """
    Обрабатывает одну новость: находит подходящее событие или создаёт новое.
    Возвращает: (обновлённая_новость, новое_событие, обновлённое_событие)
    """
    pass



# Use case для поиска кандидатов событий
async def find_event_candidates_for_raw_news(
        raw_news: RawNews,
        events_repo: NewsEventRepository,
        similarity_matcher: SimilarityMatcherService,
        config: ClusteringConfig
) -> dict[NewsEvent, float]:
    """Находит и ранжирует кандидатов событий для новости."""

    # Получаем предварительных кандидатов
    candidates = events_repo.get_news_events_candidates(raw_news, config)

    if not candidates:
        return {}

    # Получаем оценки similarity для кандидатов
    similarity_scores = await similarity_matcher.get_similar_news_candidates(
        raw_news, config
    )

    return similarity_scores


# Use case для создания нового события
async def create_new_event_from_raw_news(
        raw_news: RawNews,
        events_repo: NewsEventRepository
) -> tuple[RawNews, NewsEvent]:
    """Создаёт новое событие из сырой новости."""

    new_event = await events_repo.create_from_raw_news(raw_news)
    updated_raw = raw_news.with_event_key(new_event.id)

    return updated_raw, new_event


# Use case для присоединения к существующему событию
async def attach_raw_news_to_existing_event(
        raw_news: RawNews,
        target_event: NewsEvent,
        events_repo: NewsEventRepository
) -> tuple[RawNews, NewsEvent]:
    """Присоединяет сырую новость к существующему событию."""

    updated_event = await events_repo.attach_raw_to_existing_event(
        raw_news, target_event
    )
    updated_raw = raw_news.with_event_key(updated_event.id)

    return updated_raw, updated_event


# Use case для выбора лучшего события
async def choose_best_event_for_raw_news(
        raw_news: RawNews,
        similarity_candidates: dict[NewsEvent, float],
        similarity_matcher: SimilarityMatcherService
) -> NewsEvent | None:
    """Выбирает лучшее событие на основе similarity scores."""

    if not similarity_candidates:
        return None

    return await similarity_matcher.choose_event_for_raw_news(
        raw_news, similarity_candidates
    )


async def create_events_from_raw_news(
        raw_repo: RawNewsRepository,
        events_repo: NewsEventRepository,
        similarity_matcher: SimilarityMatcherService,
        config: ClusteringConfig,
        limit: int | None = None
) -> EventAggregationResult:
    """
    Основной use case: координирует весь процесс агрегации.
    """

    # 1. Загружаем необработанные новости
    raw_news_list = await load_pending_raw_news_for_clustering(raw_repo, limit)

    if not raw_news_list:
        return EventAggregationResult([], [], [])

    # 2. Обрабатываем пакет
    result = await process_raw_news_batch_for_events(
        raw_news_list, events_repo, similarity_matcher, config
    )

    # 3. Сохраняем результаты
    await persist_event_aggregation_results(result, raw_repo, events_repo)

    return result
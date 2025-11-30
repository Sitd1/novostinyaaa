# Шаг 1
# Создание итоговой сущности "новость"
# >>> 5. Формирование итоговой новости
#     - Создать NewsEvent из кластера raw_news
#     - Суммаризировать агрегированную новость (если нужно)
#     - Проставить финальные темы/теги/важность
#     - Подготовить финальный текст для пользователя
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, Iterable

from app.core.domain.news.entities import NewsEvent
from app.core.domain.raw_news.entities import RawNews


@dataclass(frozen=True)
class NewsEventDraft:
    """
    Промежуточный объект для сборки NewsEvent.
    """
    title: str
    summary: str
    tags: list[str]
    importance_score: float
    raw_news_items: list[RawNews]


class NewsEventFactory(Protocol):
    """
    Фабрика домена: собирает NewsEvent из драфта.
    """

    def create_from_draft(self, draft: NewsEventDraft) -> NewsEvent:
        ...


class NewsEventRepository(Protocol):
    async def save(self, event: NewsEvent) -> None:
        ...


class NewsEventSummarizationService(Protocol):
    async def summarize_cluster(self, items: list[RawNews]) -> str:
        ...


class NewsEventClassificationService(Protocol):
    async def classify(
        self,
        items: list[RawNews],
    ) -> tuple[list[str], float]:
        """
        Вернуть (tags, importance_score) для итоговой новости.
        """
        ...


class TitleGenerationService(Protocol):
    async def generate_title(self, items: list[RawNews], summary: str) -> str:
        ...


class FinalTextPreparationService(Protocol):
    async def prepare_text(self, event: NewsEvent) -> str:
        """
        Подготовить финальный текст с выводом/призывом к действию.
        """
        ...


async def create_news_event_from_cluster(
    cluster_items: list[RawNews],
    summarizer: NewsEventSummarizationService,
    classifier: NewsEventClassificationService,
    title_gen: TitleGenerationService,
    factory: NewsEventFactory,
    repo: NewsEventRepository,
) -> NewsEvent:
    """
    Use case:
    - взять кластер RawNews
    - сделать общий summary
    - проставить финальные теги и важность
    - сгенерировать заголовок
    - создать и сохранить NewsEvent.
    """
    summary = await summarizer.summarize_cluster(cluster_items)
    tags, importance_score = await classifier.classify(cluster_items)
    title = await title_gen.generate_title(cluster_items, summary)

    draft = NewsEventDraft(
        title=title,
        summary=summary,
        tags=tags,
        importance_score=importance_score,
        raw_news_items=cluster_items,
    )

    event = factory.create_from_draft(draft)
    await repo.save(event)
    return event


async def summarize_news_event(
    event: NewsEvent,
    summarizer: NewsEventSummarizationService,
    repo: NewsEventRepository,
) -> NewsEvent:
    """
    Use case:
    - пересуммаризировать уже существующий NewsEvent (если нужно).
    """
    # предполагаем, что у NewsEvent есть связь с raw_news_ids
    # и мы можем получить сами RawNews где-то выше.
    # Здесь для простоты считаем, что сам event уже содержит нужные данные.
    summary = await summarizer.summarize_cluster(event.raw_news_items)
    updated = event.with_summary(summary)
    await repo.save(updated)
    return updated


async def prepare_final_news_text(
    event: NewsEvent,
    text_service: FinalTextPreparationService,
    repo: NewsEventRepository,
) -> str:
    """
    Use case:
    - подготовить финальный текст для пользователя,
      сохранить в событии (если домен это поддерживает).
    """
    text = await text_service.prepare_text(event)
    updated = event.with_final_text(text)
    await repo.save(updated)
    return text

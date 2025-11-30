# Шаг 2
# 2. Обработка raw_news
#     - Проставить теги (tags)
#     - Сделать суммаризацию (summary)
#     - Оценить важность (importance) - ???
#     - Сделать векторизацию (embedding)
from __future__ import annotations

from typing import Protocol, Iterable, Sequence

from app.core.domain.raw_news.entities import RawNews


class TaggingService(Protocol):
    async def assign_tags(self, item: RawNews) -> list[str]:
        ...


class SummarizationService(Protocol):
    async def summarize(self, item: RawNews) -> str:
        ...


class ImportanceScoringService(Protocol):
    async def score_importance(self, item: RawNews) -> float:
        """
        Вернуть числовой скор важности (например, 0..1),
        который потом домен может маппить в ImportanceLevel.
        """
        ...


class EmbeddingService(Protocol):
    async def embed(self, item: RawNews) -> list[float]:
        ...


class RawNewsProcessingRepository(Protocol):
    """
    Репозиторий, который умеет обновлять обогащённые поля RawNews:
    tags, summary, importance, embedding.
    """

    async def list_pending_for_processing(self, limit: int | None = None) -> list[RawNews]:
        ...

    async def save(self, item: RawNews) -> None:
        ...


async def assign_tags_to_raw_news(
    repo: RawNewsProcessingRepository,
    tagging: TaggingService,
    limit: int | None = None,
) -> None:
    """
    Use case:
    - забрать RawNews, которым нужны теги
    - рассчитать теги
    - сохранить обновлённые сущности.
    """
    items = await repo.list_pending_for_processing(limit=limit)

    for item in items:
        tags = await tagging.assign_tags(item)
        item = item.with_tags(tags)  # предполагаем, что доменная сущность иммутабельна
        await repo.save(item)


async def summarize_raw_news(
    repo: RawNewsProcessingRepository,
    summarizer: SummarizationService,
    limit: int | None = None,
) -> None:
    """
    Use case:
    - забрать RawNews, которым не хватает summary
    - сделать суммаризацию
    - сохранить.
    """
    items = await repo.list_pending_for_processing(limit=limit)

    for item in items:
        summary = await summarizer.summarize(item)
        item = item.with_summary(summary)
        await repo.save(item)


async def evaluate_importance(
    repo: RawNewsProcessingRepository,
    scorer: ImportanceScoringService,
    limit: int | None = None,
) -> None:
    """
    Use case:
    - оценить важность RawNews.
    """
    items = await repo.list_pending_for_processing(limit=limit)

    for item in items:
        importance_score = await scorer.score_importance(item)
        item = item.with_importance_score(importance_score)
        await repo.save(item)


async def generate_embedding_for_raw_news(
    repo: RawNewsProcessingRepository,
    embedder: EmbeddingService,
    limit: int | None = None,
) -> None:
    """
    Use case:
    - построить embedding для RawNews.
    """
    items = await repo.list_pending_for_processing(limit=limit)

    for item in items:
        embedding = await embedder.embed(item)
        item = item.with_embedding(embedding)
        await repo.save(item)

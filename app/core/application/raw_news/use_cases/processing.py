# Шаг 2
# 2. Обработка raw_news
#     - Проставить теги (tags)
#     - Сделать суммаризацию (summary)
#     - Оценить важность (importance) - ???
#     - Сделать векторизацию (embedding)
# app/core/application/raw_news/use_cases/processing.py

from __future__ import annotations

from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.repositories import RawNewsRepository
from app.core.application.raw_news.ports import (
    TaggingService,
    SummarizationService,
    ImportanceScoringService,
    EmbeddingService,
)


async def assign_tags_to_raw_news(
    repo: RawNewsRepository,
    tagging: TaggingService,
    limit: int | None = None,
) -> None:
    items = await repo.list_pending_for_processing(limit=limit)

    for item in items:
        tags = await tagging.assign_tags(item)
        item = item.with_tags(tags)  # доменная операция
        await repo.save(item)


async def summarize_raw_news(
    repo: RawNewsRepository,
    summarizer: SummarizationService,
    limit: int | None = None,
) -> None:
    items = await repo.list_pending_for_processing(limit=limit)

    for item in items:
        summary = await summarizer.summarize(item)
        item = item.with_summary(summary)
        await repo.save(item)


async def evaluate_importance(
    repo: RawNewsRepository,
    scorer: ImportanceScoringService,
    limit: int | None = None,
) -> None:
    items = await repo.list_pending_for_processing(limit=limit)

    for item in items:
        importance_score = await scorer.score_importance(item)
        item = item.with_importance_score(importance_score)
        await repo.save(item)


async def generate_embedding_for_raw_news(
    repo: RawNewsRepository,
    embedder: EmbeddingService,
    limit: int | None = None,
) -> None:
    items = await repo.list_pending_for_processing(limit=limit)

    for item in items:
        embedding = await embedder.embed(item)
        item = item.with_embedding(embedding)
        await repo.save(item)

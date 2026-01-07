# Шаг 2
# 2. Обработка raw_news (обогащение данными) как - неважно
# а под капотом, например
#     - Проставить теги (tags)
#     - Сделать суммаризацию (summary)
#     - Оценить важность (importance) - ???
#     - Сделать векторизацию (embedding)
# app/core/application/raw_news/use_cases/processing.py

from repositories import RawNewsRepository
from processing import RawNewsEnrichmentService
from entities import RawNews


async def enrich_raw_news(
    repo: RawNewsRepository,
    enrichment: RawNewsEnrichmentService,
    limit: int | None = None,
) -> None:
    """
    Use case:
    - взять пачку RawNews, которые нуждаются в обработке
    - за один вызов сервиса получить summary/tags/importance/embedding
        (под капотом не важно как будет происходить)
    - сохранить обновлённые сущности.
    """

    # взять пачку RawNews, которые нуждаются в обработке
    items = await repo.list_pending_for_processing(limit=limit)

    # за один вызов сервиса получить summary/tags/importance/embedding
    enriched_items = []
    for item in items:
        result = await enrichment.enrich(item)

        item: RawNews = (
            item
            .with_tags(result.tags)
            .with_summary(result.summary)
            .with_importance(result.importance)
            .with_embedding(result.embedding)
        )
        enriched_items.append(item)

    # сохранить обновлённые сущности
    await repo.update_many(enriched_items)

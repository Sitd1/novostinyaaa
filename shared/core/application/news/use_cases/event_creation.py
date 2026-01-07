# Шаг 1
# Создание итоговой сущности "новость"
# >>> 5. Формирование итоговой новости
#     - Создать NewsEvent из кластера raw_news
#     - Суммаризировать агрегированную новость (если нужно)
#     - Проставить финальные темы/теги/важность
#     - Подготовить финальный текст для пользователя
from __future__ import annotations

from entities import NewsEvent
from entities import RawNews
from news_event_draft import NewsEventDraft
from event_creation import (
    NewsEventSummarizationService,
    NewsEventClassificationService,
    TitleGenerationService,
    NewsEventFactory,
    NewsEventRepository,
    FinalTextPreparationService
)



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

# Шаг 4
# 4. Работа с векторами
#     - Найти похожие raw_news (по embedding)
#     - Объединить похожие raw_news в группы (кластеризация) ---->(как указать группы?)
# Работа с RawNews закончена
from __future__ import annotations

from datetime import timedelta

from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.repositories import (
    RawNewsRepository,
    NewsEventRepository,
    SimilarityMatcherService
)
from app.core.application.raw_news.config import ClusteringConfig
from app.core.domain.news.entities import NewsEvent


async def cluster_pending_raw_news(
    raw_repo: RawNewsRepository,
    events_repo: NewsEventRepository,
    similarity_matcher: SimilarityMatcherService,
    config: ClusteringConfig | None = None,
    limit: int | None = None,
) -> None:
    """
    Use case:
    - забрать пачку RawNews, у которых есть embedding, но ещё нет события
    - для каждой найти похожие новости по embedding в окне по времени
    - решить: присоединить к существующему событию или создать новое.
    """
    if config is None:
        config = ClusteringConfig()
    # --------------------------------------------------------------------------------
    # --- 1. забрать пачку RawNews по фильтру (у которых есть embedding, но ещё нет события)
    # --------------------------------------------------------------------------------
    items: list[RawNews] = await raw_repo.list_pending_for_event_clustering(limit=limit)

    # создаем события
    updated_raw_news = []  # связываем raw_news и event
    new_events = []
    updated_events = []

    # --------------------------------------------------------------------------------
    # --- 3. Обработка каждой сырой новости
    # --------------------------------------------------------------------------------
    for raw in items:

        # Интуиция: Если time_window_before = 24 часа,
        # то для новости в 15:00 мы смотрим события примерно с 15:00 вчера до 15:00 сегодня.
        window_start = raw.published_at - config.time_window_before  # timedelta
        window_end = raw.published_at + config.time_window_after  # timedelta

        # 3.2. Ищем кандидаты-события - получить небольшой список событий,
        # с которыми можно сравнить текущую новость


        # смотрим ближайшие и косинусное расстояние отсеиваем по threshold также смотрим прочие фильтры
        event_candidates: list[NewsEvent] = events_repo.get_news_events_candidates(raw, config) # совпадение по диапазону времени window_start, window_end и прочее по конфигу

        if event_candidates:
            similarity_candidates: dict[int, int] = await similarity_matcher.get_similar_news_candidates(raw, config)
        else:
            similarity_candidates: dict[int, int] = dict()

        # Создание нового события (нет подходящих events)
        if len(similarity_candidates.keys()) == 0:
            event = await events_repo.create_from_raw_news(raw)  # новое событие
            new_events.append(event)
            # У raw появляется ссылка на это событие (на уровне доменной логики) — «я теперь в этом событии». event_id
            # Это событие и обновлённая новость откладываются для последующего сохранения
        # Добавление события к
        else:
            # {event_id: similarity_with_raw_news} -> выбираем самое близкое событие или еще просим llm сопоставить с пачкой
            # принимаем решение создать Event или прикрепить новость к старом Event
            #

            # пропускаем кандидаты через ллм и проверяем (небольшую) пачку подходит это или нет
            # я бы всё же это просто сделал на стороне агентов # todo: del this comment
            chosen_event = await similarity_matcher.similaritychoose_event_for_raw_news(raw, similarity_candidates)
            if chosen_event is None:
                event = await events_repo.create_from_raw_news(raw)
                new_events.append(event)
            else:
                event = await events_repo.attach_raw_to_existing_event(raw, chosen_event)
                updated_events.append(event)

        # обновляем только raw приписывая event_id в качестве fk
        raw = raw.with_event_key(event.id)
        updated_raw_news.append(raw)

    # --------------------------------------------------------------------------------
    # --- 4. Сохранение результатов
    # --------------------------------------------------------------------------------
    await raw_repo.update_many(updated_raw_news)  # обновляем raw_repo
    await events_repo.update_many(updated_events)
    await events_repo.save_many(new_events)

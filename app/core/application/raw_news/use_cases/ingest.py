# Шаг 1
# --- ingest - процесс получения "сырого" внешнего входа → преобразования → сохранения в хранилище.
# 1. Приём сырых новостей из внешнего источника
# IngestRawNewsBatch
# Вход: список сообщений из Telegram/других источников
# Действия: создать RawNews для каждого, сохранить в репозиторий, отфильтровать дубли по внешнему id
# Выход: список новых RawNews, которые попали в систему


from app.core.application.raw_news.dto.external_raw_news_item import ExternalRawNewsItem
from app.core.application.raw_news.ports.ingest import ExternalRawNewsSource
from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.repositories import RawNewsRepository
from app.core.domain.raw_news.services import RawNewsFactory


async def ingest_new_raw_news(
        source: ExternalRawNewsSource,
        factory: RawNewsFactory,
        repo: RawNewsRepository,
) -> int:
    """
    Основной use-case:
    1. Забирает новые raw news из внешнего источника (порт)
    2. Превращает DTO в доменные RawNews (фабрика)
    3. Сохраняет доменные RawNews пачкой через репозиторий

    Returns:
        Количество сохранённых новостей
    """
    raw_news_list: list[RawNews] = []

    # 1. Получаем DTO и превращаем в доменные сущности
    async for raw_item in source.fetch_new_raw_items():
        raw_news = factory.create_from_external_item(raw_item)
        raw_news_list.append(raw_news)

    # 2. Сохраняем пачкой
    if raw_news_list:
        await repo.save_many(raw_news_list)

    return len(raw_news_list)


async def fetch_new_raw_news(
        source: ExternalRawNewsSource,
) -> list[ExternalRawNewsItem]:
    """
    Забрать новые сырые сообщения из внешнего источника в виде DTO.
    Это ещё НЕ доменные сущности, просто транспортный слой.
    (вспомогательная функция для тестирования)
    """
    items = []
    async for item in source.fetch_new_raw_items():
        items.append(item)
    return items

# --- ingest - процесс получения "сырого" внешнего входа → преобразования → сохранения в хранилище.
# 1. Приём сырых новостей из внешнего источника
# IngestRawNewsBatch
# Вход: список сообщений из Telegram/других источников
# Действия: создать RawNews для каждого, сохранить в репозиторий, отфильтровать дубли по внешнему id
# Выход: список новых RawNews, которые попали в систему

from datetime import datetime
from app.core.domain.raw_news.entities import RawNews
from app.core.domain.raw_news.value_objects import RawNewsId, ExternalMessageId, Url, RawPublishedAt, RawFetchedAt, \
    RawNewsText, Source
from app.core.domain.raw_news.repositories import RawNewsRepository

class IngestRawNewsUseCase:
    def __init__(self, raw_repo: RawNewsRepository):
        self.raw_repo = raw_repo

    async def execute(self, *, external_id: int, source: str, text: str, created_at: datetime) -> RawNews:
        # здесь ты превращаешь «грязные» данные из внешнего мира → VO
        news = RawNews(
            id=RawNewsId(external_id),
            source=Source(source),
            text=RawNewsText(text),

        )
        await self.raw_repo.add(news)
        return news

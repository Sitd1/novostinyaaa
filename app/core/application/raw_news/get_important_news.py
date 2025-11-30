"""Здесь будет находиться логика как вытаскивать важные новости для дальнейшей обработки с сбора
"""


class GetImportantNewsUseCase:
    def __init__(self, news_repo: NewsEventRepository):
        self.news_repo = news_repo

    async def execute(self, *, limit: int = 20):
        # в реализации репозитория будет условие importance >= HIGH и сортировка
        return await self.news_repo.list_recent(limit=limit)

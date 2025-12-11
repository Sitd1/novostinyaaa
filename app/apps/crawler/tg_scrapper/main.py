# Скрипт, который раз в N минут тянет новости из TG и кладёт в БД →
# app/apps/crawler/tg_scrapper/main.py
# (внутри: создаём реализации портов из infra, вызываем use-case ingest_raw_news).


# from app.infrastructure.db.session import get_session
# from app.infrastructure.db.repositories.raw_news import SqlAlchemyRawNewsRepository
# from app.infrastructure.crawler.raw_news_source import TelegramChannelRawNewsSource
# from app.core.application.raw_news.use_cases.ingest import ingest_raw_news
#
# async def main():
#     async with get_session() as session:
#         repo = SqlAlchemyRawNewsRepository(session)
#         source = TelegramChannelRawNewsSource(...config...)
#         await ingest_raw_news(source=source, repo=repo)

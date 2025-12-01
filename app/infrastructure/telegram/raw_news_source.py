# Реализуем порт из core:
# ExternalRawNewsSource и DTO ExternalRawNewsItem у тебя в
# app/core/application/raw_news/dto/external_raw_news_item.py и
# .../ports/ingest.py.

# async def fetch_new_raw_items(self) -> Iterable[ExternalRawNewsItem]:
#     # использует client.fetch_channel_messages(...)
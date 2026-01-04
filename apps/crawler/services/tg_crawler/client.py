# agents_service/telegram_raw/client.py
from telethon import TelegramClient
from apps.crawler.crawler_config import tg_crawler_config


def get_telegram_client() -> TelegramClient:
    """
    Создаёт и возвращает Telethon клиент.
    Сессия будет храниться в файле SESSION_NAME.session
    """
    return TelegramClient(
        tg_crawler_config.session_name,
        int(tg_crawler_config.api_id.get_secret_value()),
        tg_crawler_config.api_hash.get_secret_value(),
    )

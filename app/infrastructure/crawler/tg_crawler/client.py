# agents_service/telegram_raw/client.py
from telethon import TelegramClient
from app.config import crawler_config



def get_telegram_client() -> TelegramClient:
    """
    Создаёт и возвращает Telethon клиент.
    Сессия будет храниться в файле SESSION_NAME.session
    """
    return TelegramClient(
        crawler_config.telegram_config.session_name,
        int(crawler_config.telegram_config.api_id.get_secret_value()),
        crawler_config.telegram_config.api_hash.get_secret_value(),
    )

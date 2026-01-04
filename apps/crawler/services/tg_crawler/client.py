# agents_service/telegram_raw/client.py
from telethon import TelegramClient
from shared.config import config

tg_scr_config = config.telegram

def get_telegram_client() -> TelegramClient:
    """
    Создаёт и возвращает Telethon клиент.
    Сессия будет храниться в файле SESSION_NAME.session
    """
    return TelegramClient(
        tg_scr_config.session_name,
        int(tg_scr_config.api_id.get_secret_value()),
        tg_scr_config.api_hash.get_secret_value(),
    )

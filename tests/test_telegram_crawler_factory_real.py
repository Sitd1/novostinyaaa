#!/usr/bin/env python3
"""
Тест для проверки работоспособности функции create_telegram_raw_news_source с реальным Telegram клиентом.
"""
import asyncio
import os
import sys
from pathlib import Path
from unittest.mock import AsyncMock

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from telethon import TelegramClient
from app.infrastructure.crawler.tg_crawler.factory import create_telegram_raw_news_source
from app.infrastructure.crawler.tg_crawler.raw_news_source import TelegramRawNewsSource
from app.infrastructure.database.repositories.tg_raw_news import TgRawNewsRepository


def check_telegram_config():
    """Проверяем, что переменные окружения для Telegram настроены."""
    api_id = os.getenv('CRAWLER_TG_API_ID')
    api_hash = os.getenv('CRAWLER_TG_API_HASH')
    session_name = os.getenv('CRAWLER_TG_SESSION_NAME')

    if not api_id or not api_hash or not session_name:
        print("⚠️  Переменные окружения Telegram не настроены!")
        print("   Требуются: CRAWLER_TG_API_ID, CRAWLER_TG_API_HASH, CRAWLER_TG_SESSION_NAME")
        print("   Проверьте файл .env")
        return False

    print("✅ Переменные окружения Telegram настроены")
    return True


async def test_create_telegram_raw_news_source_real():
    """Тест создания TelegramRawNewsSource через фабрику с реальным Telegram клиентом."""
    print("Тестируем функцию create_telegram_raw_news_source с реальным клиентом...")

    # Создаем mock сессию
    mock_session = AsyncMock()

    try:
        # Вызываем функцию фабрики с реальным клиентом
        result = await create_telegram_raw_news_source(mock_session)

        # Проверяем тип результата
        assert isinstance(result, TelegramRawNewsSource), f"Ожидался TelegramRawNewsSource, получен {type(result)}"

        # Проверяем, что объект правильно инициализирован
        assert hasattr(result, 'client'), "Объект должен иметь атрибут client"
        assert hasattr(result, 'repo'), "Объект должен иметь атрибут repo"
        assert hasattr(result, 'channels'), "Объект должен иметь атрибут channels"
        assert hasattr(result, 'limit_per_channel'), "Объект должен иметь атрибут limit_per_channel"

        # Проверяем типы атрибутов
        assert isinstance(result.client, TelegramClient), f"client должен быть TelegramClient, получен {type(result.client)}"
        assert isinstance(result.repo, TgRawNewsRepository), f"repo должен быть TgRawNewsRepository, получен {type(result.repo)}"

        # Проверяем значения
        assert result.limit_per_channel == 50, f"limit_per_channel должен быть 50, получен {result.limit_per_channel}"
        assert len(result.channels) > 0, "Должен быть хотя бы один канал"

        print("✅ Функция create_telegram_raw_news_source с реальным клиентом работает корректно!")
        print(f"   Тип результата: {type(result)}")
        print(f"   Тип клиента: {type(result.client)}")
        print(f"   limit_per_channel: {result.limit_per_channel}")
        print(f"   Количество каналов: {len(result.channels)}")
        print(f"   Каналы: {result.channels}")

        return True

    except Exception as e:
        print(f"❌ Ошибка при выполнении функции с реальным клиентом: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_imports():
    """Тест, что все импорты работают."""
    print("Тестируем импорты...")

    try:
        # Проверяем импорты
        from app.infrastructure.crawler.tg_crawler.factory import create_telegram_raw_news_source
        from app.infrastructure.crawler.tg_crawler.raw_news_source import TelegramRawNewsSource
        from app.infrastructure.database.repositories.tg_raw_news import TgRawNewsRepository
        from app.infrastructure.crawler.tg_crawler.client import get_telegram_client
        from telethon import TelegramClient

        print("✅ Все импорты успешны!")
        return True

    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        return False


async def main():
    """Главная функция теста."""
    print("🚀 Начинаем тестирование функции create_telegram_raw_news_source с реальным клиентом")
    print()

    # Проверяем конфигурацию Telegram
    if not check_telegram_config():
        print("❌ Тест пропущен - нет конфигурации Telegram")
        return False

    print()

    # Тест импортов
    imports_ok = await test_imports()
    if not imports_ok:
        return False

    print()

    # Тест функции с реальным клиентом
    function_ok = await test_create_telegram_raw_news_source_real()
    if not function_ok:
        return False

    print()
    print("🎉 Все тесты с реальным клиентом пройдены успешно!")
    return True


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
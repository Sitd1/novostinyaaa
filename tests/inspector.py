#!/usr/bin/env python3
"""
Инспектор объекта TelegramRawNewsSource для детального анализа.
"""
import asyncio
import sys
from pathlib import Path
from pprint import pprint

# Добавляем корневую директорию проекта в PYTHONPATH
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from unittest.mock import AsyncMock
from app.infrastructure.crawler.tg_crawler.factory import create_telegram_raw_news_source


async def inspect_telegram_raw_news_source():
    """Детальный анализ объекта TelegramRawNewsSource."""
    print("🔍 Детальный анализ объекта TelegramRawNewsSource")
    print("=" * 60)

    # Создаем mock сессию
    mock_session = AsyncMock()

    # Создаем объект
    source = await create_telegram_raw_news_source(mock_session)

    print(f"Тип объекта: {type(source)}")
    print(f"Модуль: {source.__class__.__module__}")
    print()

    # Основные атрибуты
    print("📋 Основные атрибуты:")
    print(f"  client: {type(source.client)}")
    print(f"  repo: {type(source.repo)}")
    print(f"  channels: {source.channels} (тип: {type(source.channels)})")
    print(f"  limit_per_channel: {source.limit_per_channel} (тип: {type(source.limit_per_channel)})")
    print()

    # Методы объекта
    print("🔧 Доступные методы:")
    methods = [method for method in dir(source) if not method.startswith('_') and callable(getattr(source, method))]
    for method in methods:
        print(f"  {method}")
    print()

    # Информация о клиенте
    print("📱 Информация о Telegram клиенте:")
    print(f"  Тип: {type(source.client)}")
    if hasattr(source.client, 'api_id'):
        print(f"  API ID: {source.client.api_id}")
    if hasattr(source.client, 'session'):
        print(f"  Сессия: {type(source.client.session)}")
    print()

    # Информация о репозитории
    print("💾 Информация о репозитории:")
    print(f"  Тип: {type(source.repo)}")
    print(f"  Сессия: {type(source.repo.session)}")
    print()

    # Структура объекта
    print("🏗️  Структура объекта (атрибуты):")
    attrs = {}
    for attr in dir(source):
        if not attr.startswith('_'):
            value = getattr(source, attr)
            if not callable(value):
                attrs[attr] = f"{type(value).__name__}: {repr(value) if len(repr(value)) < 100 else str(type(value)) + ' (too long)'}"

    for attr, info in attrs.items():
        print(f"  {attr}: {info}")
    print()

    # Проверяем интерфейс
    print("🔌 Проверка интерфейса ExternalRawNewsSource:")
    print(f"  Имеет fetch_new_raw_items: {hasattr(source, 'fetch_new_raw_items')}")

    if hasattr(source, 'fetch_new_raw_items'):
        method = getattr(source, 'fetch_new_raw_items')
        print(f"  fetch_new_raw_items - callable: {callable(method)}")
        print(f"  fetch_new_raw_items - async: {asyncio.iscoroutinefunction(method)}")

    # Проверяем сигнатуру метода
    import inspect
    try:
        sig = inspect.signature(source.fetch_new_raw_items)
        print(f"  Сигнатура fetch_new_raw_items: {sig}")
    except Exception as e:
        print(f"  Не удалось получить сигнатуру: {e}")

    print()
    print("✅ Анализ завершен!")


if __name__ == "__main__":
    asyncio.run(inspect_telegram_raw_news_source())

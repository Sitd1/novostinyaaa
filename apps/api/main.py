from fastapi import FastAPI, BackgroundTasks
from datetime import datetime
import logging

from apps.crawler.services.tg_crawler.probe_collect import collect_last_messages

app = FastAPI(title="Novostinya API")
logger = logging.getLogger(__name__)


@app.get("/")
async def root():
    return {"status": "ok", "service": "novostinya-api"}


@app.post("/crawler/run")
async def run_crawler(
        background_tasks: BackgroundTasks,
        limit_per_channel: int = 50
):
    """Запустить сбор новостей из Telegram"""

    def crawl():
        try:
            logger.info(f"Запущен сбор сообщений: limit={limit_per_channel}")
            result = collect_last_messages(limit_per_channel=limit_per_channel)
            logger.info(f"Сбор завершен: {result}")
        except Exception as e:
            logger.error(f"Ошибка при сборе: {e}", exc_info=True)

    background_tasks.add_task(crawl)

    return {
        "status": "started",
        "timestamp": datetime.now().isoformat(),
        "limit_per_channel": limit_per_channel
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}
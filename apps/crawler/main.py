import asyncio

from apps.crawler.services.tg_crawler.probe_collect import collect_last_messages


def main():
    asyncio.run(collect_last_messages(limit_per_channel=50))


if __name__ == "__main__":
    main()
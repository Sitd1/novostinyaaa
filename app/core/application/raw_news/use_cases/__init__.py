# Пример шаблона use-case
# async def some_use_case(
#     repo: SomethingRepository,
#     service: SomeDomainService,
#     limit: int | None = None,
# ) -> None:
#
#     # 1. получить данные
#     items = await repo.list_pending(limit=limit)
#
#     # 2. обработать
#     for item in items:
#         updated = service.process(item)  # доменная логика внутри
#         await repo.save(updated)

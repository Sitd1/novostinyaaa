# 9. Обновление статуса обработки raw_news
# MarkRawNewsProcessingStage
# Вход: RawNews + новый статус (ingested / scored / tagged / summarized / vectorized / ready_for_aggregation, и т.п.)
# Действия: обновить поля статуса обработки
# Выход: обновлённая RawNews
# Смысл: уметь по состоянию понять, какие шаги по raw_news уже выполнены
# Юзкейс: *«Отфильтровать важные новости»*.
#
# * Берёт `RawNewsRepository` и `NewsRepository`.
# * Берёт `AgentsService` / `ImportanceScorer` (абстракция поверх LLM).
# * Прогоняет новости через агента, получает оценку важности.
# * Создаёт доменные `News` из `RawNews` с признаком важности.
# * Сохраняет в `NewsRepository`.
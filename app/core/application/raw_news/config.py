from dataclasses import dataclass
from datetime import timedelta


@dataclass(frozen=True)
class ClusteringConfig:
    similarity_threshold: float = 0.82
    time_window: timedelta = timedelta(hours=24)
    top_k_neighbors: int = 20
    min_news_count: int = 1


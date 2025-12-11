from dotenv import load_dotenv
from pydantic_settings import SettingsConfigDict
from pydantic import SecretStr, Field

from app.config.base_configs.base import ConfigBase


load_dotenv()


class TelegramConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="CRAWLER_TG_")  # FixMe: переделать как нужно в .env

    api_id: SecretStr
    api_hash: SecretStr
    session_name: str


class CrawlerConfig(ConfigBase):
    telegram_config: TelegramConfig = Field(default_factory=TelegramConfig)


crawler_config = CrawlerConfig()

# if __name__ == "__main__":
#     print(crawler_config.telegram_config)

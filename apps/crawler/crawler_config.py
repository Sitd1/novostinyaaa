from dotenv import load_dotenv
from pydantic_settings import SettingsConfigDict
from pydantic import SecretStr

from shared.config.base_configs.base import ConfigBase


load_dotenv()


class TgCrawlerConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="CRAWLER_TG_")

    api_id: SecretStr
    api_hash: SecretStr
    session_name: str



tg_crawler_config = TgCrawlerConfig()

if __name__ == "__main__":
    print(TgCrawlerConfig())

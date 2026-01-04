from dotenv import load_dotenv
from pydantic_settings import SettingsConfigDict
from pydantic import SecretStr

from base_configs.base import ConfigBase


load_dotenv()


class CrawlerConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="CRAWLER_TG_")

    api_id: SecretStr
    api_hash: SecretStr
    session_name: str


crawler_config = CrawlerConfig()

# if __name__ == "__main__":
#     print(crawler_config)

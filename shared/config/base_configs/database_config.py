from dotenv import load_dotenv
from pydantic_settings import SettingsConfigDict
from pydantic import SecretStr

from shared.config.base_configs.base import ConfigBase


load_dotenv()


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="db_")

    user: str
    password: SecretStr
    name: str
    host: str
    port: int


    @property
    def url_asyncpg(self) -> str:
        """PostgreSQL URL для asyncpg"""
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"

    @property
    def url_psycopg(self) -> str:
        """PostgreSQL URL для psycopg"""
        return f"postgresql+psycopg2://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.name}"

database_config = DatabaseConfig()


# if __name__ == "__main__":
#     print(database_config)

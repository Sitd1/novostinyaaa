from dotenv import load_dotenv
from pydantic_settings import SettingsConfigDict
from pydantic import SecretStr

from base_configs.base import ConfigBase


load_dotenv()


class TgBotConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="TELEGRAM_")

    bot_token: SecretStr
    channel_id: str

tg_bot_config = TgBotConfig()


# if __name__ == "__main__":
#     print(tg_bot_config)

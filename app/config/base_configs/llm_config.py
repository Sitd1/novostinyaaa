from dotenv import load_dotenv
from pydantic_settings import SettingsConfigDict
from pydantic import SecretStr, Field

from app.config.base_configs.base import ConfigBase


load_dotenv()


# LLM Agent
class BaseLLMConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="LLM_")

    api_key: SecretStr
    base_url: str
    model: str


# Perplexity
class PPLXConfig(BaseLLMConfig):
    model_config = SettingsConfigDict(env_prefix="PPLX_")


# Tavily
class TavilyConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="TAVILY_")
    api_key: SecretStr


class LLMConfig(ConfigBase):
    base_llm: BaseLLMConfig = Field(default_factory=BaseLLMConfig)
    pplx: PPLXConfig = Field(default_factory=PPLXConfig)
    tavily: TavilyConfig = Field(default_factory=TavilyConfig)


llm_config = LLMConfig()

# if __name__ == "__main__":
#     print(llm_config)

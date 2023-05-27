from pydantic import BaseConfig, BaseSettings


class TelegramSettings(BaseSettings):
    token: str
    pay_token: str

    class Config(BaseConfig):
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "telegram_"

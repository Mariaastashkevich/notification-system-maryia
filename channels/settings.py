from pydantic_settings import BaseSettings, SettingsConfigDict


# TODO: перевести на pydantic.BaseSettings позже, чтобы:
# TODO: читать из .env
# TODO: закрыть пункт Configuration целиком


class ChannelSettings(BaseSettings):
    sms_enabled: bool = True
    email_enabled: bool = True
    sms_failure_rate: float = 0.0
    email_failure_rate: float = 0.0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


from pydantic_settings import BaseSettings, SettingsConfigDict


class ChannelSettings(BaseSettings):
    sms_enabled: bool = True
    email_enabled: bool = True
    sms_failure_rate: float = 0.0
    email_failure_rate: float = 0.0

    model_config = SettingsConfigDict(
        env_file=".env.example",
        extra="ignore"
    )

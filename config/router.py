import json
from typing import Dict, List

from pydantic_settings import BaseSettings, SettingsConfigDict

from core.notification_message import Priority


class RouterSettings(BaseSettings):
    fallback_enabled: bool = True

    channel_priority: str = (
        '{"LOW": ["sms"], '
        '"NORMAL": ["sms"], '
        '"HIGH": ["sms", "email"], '
        '"CRITICAL": ["sms", "email"]}'
    )

    model_config = SettingsConfigDict(
        env_file=".env.example",
        extra="ignore"
    )

    def priority_to_dict(self) -> Dict[Priority, List[str]]:
        raw = json.loads(self.channel_priority)
        return {
            Priority[key]: value for key, value in raw.items()
        }





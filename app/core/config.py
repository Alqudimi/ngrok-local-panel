import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "Ngrok Local Control Panel"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = Field(default="super-secret-key-change-me", validation_alias="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Ngrok Settings
    NGROK_PATH: str = Field(default="ngrok", validation_alias="NGROK_PATH")
    NGROK_CONFIG_DIR: str = "config"
    NGROK_LOG_DIR: str = "logs"
    NGROK_DATA_DIR: str = "data"
    
    # Security
    API_KEY: Optional[str] = Field(default=None, validation_alias="API_KEY")
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Webhooks
    DISCORD_WEBHOOK_URL: Optional[str] = Field(default=None, validation_alias="DISCORD_WEBHOOK_URL")
    TELEGRAM_BOT_TOKEN: Optional[str] = Field(default=None, validation_alias="TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID: Optional[str] = Field(default=None, validation_alias="TELEGRAM_CHAT_ID")

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True)

settings = Settings()

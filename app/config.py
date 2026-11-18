"""Application configuration settings using pydantic-settings."""

from typing import Literal, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for FastAPI Application."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 4000
    DEBUG: bool = False

    # LLM Settings (100% Free Default: local_ai; optional free tier: gemini, groq)
    LLM_PROVIDER: str = "local_ai"
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.5-flash"

    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"

    # Scraping & HTTP client limits
    SCRAPER_TIMEOUT_SECONDS: float = 12.0
    SCRAPER_MAX_BODY_CHARS: int = 25000
    USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 (AntigravityLinkAnalyzer/1.0)"
    )

    # Multi-platform posting settings (Simulation mode provides instant free testing)
    POSTING_SIMULATION_MODE: bool = True

    # 100% Free Platform Credentials (Optional for live delivery)
    # 1. Telegram
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    TELEGRAM_CHAT_ID: Optional[str] = None

    # 2. Discord
    DISCORD_WEBHOOK_URL: Optional[str] = None

    # 3. Slack
    SLACK_WEBHOOK_URL: Optional[str] = None

    # 4. Mastodon
    MASTODON_INSTANCE_URL: str = "https://mastodon.social"
    MASTODON_ACCESS_TOKEN: Optional[str] = None

    # 5. Bluesky
    BLUESKY_HANDLE: Optional[str] = None
    BLUESKY_APP_PASSWORD: Optional[str] = None

    # 6. X (Twitter)
    TWITTER_BEARER_TOKEN: Optional[str] = None


settings = Settings()

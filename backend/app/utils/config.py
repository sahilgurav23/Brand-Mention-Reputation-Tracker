"""Configuration settings for the application"""
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # Database
    database_url: str = "postgresql://tracker:password123@localhost:5432/trackerdb"

    # API Keys (load from environment)
    twitter_api_key: str = ""
    twitter_api_secret: str = ""
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    news_api_key: str = ""

    # Brand configuration
    brand_name: str = ""
    brand_keywords: str = ""
    search_query: str = ""

    # ML Models
    sentiment_model: str = "distilbert-base-uncased-finetuned-sst-2-english"
    embedding_model: str = "all-MiniLM-L6-v2"

    # Alert Settings
    alert_threshold: float = 2.5  # Standard deviations
    alert_window_hours: int = 24

    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
    ]

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

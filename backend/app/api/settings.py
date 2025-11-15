"""Settings API endpoints

This module exposes a minimal API to read and update runtime settings
such as API keys and brand configuration. Settings are stored in a
single-row table in PostgreSQL so they can be edited from the UI.
"""

from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.models.database import get_db, engine
from app.utils.config import settings as default_settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


class SettingsPayload(BaseModel):
    """Payload used by the settings UI.

    Only includes values that are safe and useful to edit from the
    dashboard, not low-level database configuration.
    """

    news_api_key: Optional[str] = None
    twitter_api_key: Optional[str] = None
    twitter_api_secret: Optional[str] = None
    reddit_client_id: Optional[str] = None
    reddit_client_secret: Optional[str] = None
    brand_name: Optional[str] = None
    brand_keywords: Optional[str] = None
    search_query: Optional[str] = None


def ensure_settings_table_exists() -> None:
    """Create the app_settings table if it does not already exist.

    This keeps things simple so you do not need to run a separate
    migration command just to store UI-editable settings.
    """

    ddl = text(
        """
        CREATE TABLE IF NOT EXISTS app_settings (
            id SERIAL PRIMARY KEY,
            news_api_key TEXT,
            twitter_api_key TEXT,
            twitter_api_secret TEXT,
            reddit_client_id TEXT,
            reddit_client_secret TEXT,
            brand_name TEXT,
            brand_keywords TEXT,
            search_query TEXT,
            created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
            updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW()
        );
        """
    )
    with engine.begin() as conn:
        conn.execute(ddl)


@router.get("", response_model=SettingsPayload)
async def get_settings(db: Session = Depends(get_db)) -> SettingsPayload:
    """Return the current editable settings.

    If there is no row yet, this falls back to the values from
    ``app.utils.config.settings`` and does not create anything.
    """

    ensure_settings_table_exists()

    row = db.execute(
        text(
            "SELECT news_api_key, twitter_api_key, twitter_api_secret, reddit_client_id, reddit_client_secret, brand_name, brand_keywords, search_query FROM app_settings ORDER BY id LIMIT 1"
        )
    ).fetchone()

    if not row:
        # No DB row yet: fall back to config defaults so the UI is not empty.
        return SettingsPayload(
            news_api_key=default_settings.news_api_key or None,
            twitter_api_key=default_settings.twitter_api_key or None,
            twitter_api_secret=default_settings.twitter_api_secret or None,
            reddit_client_id=default_settings.reddit_client_id or None,
            reddit_client_secret=default_settings.reddit_client_secret or None,
            brand_name=default_settings.brand_name or None,
            brand_keywords=default_settings.brand_keywords or None,
            search_query=default_settings.search_query or None,
        )

    return SettingsPayload(
        news_api_key=row[0],
        twitter_api_key=row[1],
        twitter_api_secret=row[2],
        reddit_client_id=row[3],
        reddit_client_secret=row[4],
        brand_name=row[5],
        brand_keywords=row[6],
        search_query=row[7],
    )


@router.put("", response_model=SettingsPayload)
async def update_settings(payload: SettingsPayload, db: Session = Depends(get_db)) -> SettingsPayload:
    """Create or update the single settings row.

    The UI will call this when you click "Save" on the settings page.
    """

    ensure_settings_table_exists()

    now = datetime.utcnow()

    # Check if a row already exists.
    row = db.execute(text("SELECT id FROM app_settings ORDER BY id LIMIT 1")).fetchone()

    if row:
        # Update existing row.
        db.execute(
            text(
                """
                UPDATE app_settings
                SET news_api_key = :news_api_key,
                    twitter_api_key = :twitter_api_key,
                    twitter_api_secret = :twitter_api_secret,
                    reddit_client_id = :reddit_client_id,
                    reddit_client_secret = :reddit_client_secret,
                    brand_name = :brand_name,
                    brand_keywords = :brand_keywords,
                    search_query = :search_query,
                    updated_at = :updated_at
                WHERE id = :id
                """
            ),
            {
                "id": row[0],
                "news_api_key": payload.news_api_key,
                "twitter_api_key": payload.twitter_api_key,
                "twitter_api_secret": payload.twitter_api_secret,
                "reddit_client_id": payload.reddit_client_id,
                "reddit_client_secret": payload.reddit_client_secret,
                "brand_name": payload.brand_name,
                "brand_keywords": payload.brand_keywords,
                "search_query": payload.search_query,
                "updated_at": now,
            },
        )
    else:
        # Insert new row.
        db.execute(
            text(
                """
                INSERT INTO app_settings (
                    news_api_key,
                    twitter_api_key,
                    twitter_api_secret,
                    reddit_client_id,
                    reddit_client_secret,
                    brand_name,
                    brand_keywords,
                    search_query,
                    created_at,
                    updated_at
                )
                VALUES (
                    :news_api_key,
                    :twitter_api_key,
                    :twitter_api_secret,
                    :reddit_client_id,
                    :reddit_client_secret,
                    :brand_name,
                    :brand_keywords,
                    :search_query,
                    :created_at,
                    :updated_at
                )
                """
            ),
            {
                "news_api_key": payload.news_api_key,
                "twitter_api_key": payload.twitter_api_key,
                "twitter_api_secret": payload.twitter_api_secret,
                "reddit_client_id": payload.reddit_client_id,
                "reddit_client_secret": payload.reddit_client_secret,
                "brand_name": payload.brand_name,
                "brand_keywords": payload.brand_keywords,
                "search_query": payload.search_query,
                "created_at": now,
                "updated_at": now,
            },
        )

    db.commit()

    logger.info("Settings updated via API")
    return payload

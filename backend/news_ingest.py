"""One-off script to ingest news articles into the ``mentions`` table.

Usage (from backend folder, with venv active)::

    python news_ingest.py

High-level flow:
- Read brand search settings from ``app.utils.config.settings``.
- Call NewsAPI via ``app.services.aggregator.aggregate_from_news`` to fetch articles.
- Run sentiment + topic classification for each article.
- Insert rows into the ``mentions`` table so the API + dashboard can see data.

This script is intentionally simple so you can understand the full pipeline
from external API -> processing -> database.
"""

import asyncio
from datetime import datetime
from typing import List, Dict

from dateutil.parser import isoparse
from sqlalchemy import text

from app.models.database import Mention, SessionLocal
from app.services.aggregator import aggregate_all_sources
from app.services.clustering import get_topic_for_mention
from app.services.sentiment import analyze_sentiment
from app.services.alerts import run_basic_alert_checks
from app.utils.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


def load_effective_settings() -> Dict[str, str]:
    """Load editable settings from the app_settings table if present.

    Values saved from the /settings UI are stored in app_settings. If
    that table or its row does not exist yet, we fall back to
    app.utils.config.settings (i.e. .env) so ingestion still works.
    """

    db = SessionLocal()
    try:
        row = db.execute(
            text(
                "SELECT news_api_key, twitter_api_key, twitter_api_secret, "
                "reddit_client_id, reddit_client_secret, brand_name, brand_keywords, search_query "
                "FROM app_settings ORDER BY id LIMIT 1"
            )
        ).fetchone()

        if row:
            return {
                "news_api_key": row[0] or settings.news_api_key,
                "twitter_api_key": row[1] or settings.twitter_api_key,
                "twitter_api_secret": row[2] or settings.twitter_api_secret,
                "reddit_client_id": row[3] or settings.reddit_client_id,
                "reddit_client_secret": row[4] or settings.reddit_client_secret,
                "brand_name": row[5] or settings.brand_name,
                "brand_keywords": row[6] or settings.brand_keywords,
                "search_query": row[7] or settings.search_query,
            }

        # No DB row yet: fall back entirely to config.
        return {
            "news_api_key": settings.news_api_key,
            "twitter_api_key": settings.twitter_api_key,
            "twitter_api_secret": settings.twitter_api_secret,
            "reddit_client_id": settings.reddit_client_id,
            "reddit_client_secret": settings.reddit_client_secret,
            "brand_name": settings.brand_name,
            "brand_keywords": settings.brand_keywords,
            "search_query": settings.search_query,
        }
    finally:
        db.close()


async def ingest_news_mentions() -> None:
    """Fetch mentions from all configured sources and store them.

    The goal is to populate the ``mentions`` table so that:
    - ``/api/mentions`` returns real rows.
    - ``/api/analytics/*`` endpoints have something to aggregate.
    """

    # 1) Load effective settings (prefer values edited from the /settings UI).
    effective = load_effective_settings()

    # Keep the global settings object in sync for downstream services
    # such as aggregate_* functions, which read from app.utils.config.settings.
    if effective.get("news_api_key"):
        settings.news_api_key = effective["news_api_key"]  # type: ignore[assignment]
    if effective.get("twitter_api_key"):
        settings.twitter_api_key = effective["twitter_api_key"]  # type: ignore[assignment]
    if effective.get("twitter_api_secret"):
        settings.twitter_api_secret = effective["twitter_api_secret"]  # type: ignore[assignment]
    if effective.get("reddit_client_id"):
        settings.reddit_client_id = effective["reddit_client_id"]  # type: ignore[assignment]
    if effective.get("reddit_client_secret"):
        settings.reddit_client_secret = effective["reddit_client_secret"]  # type: ignore[assignment]

    # Decide what query to send to NewsAPI.
    # We try, in order: search_query, brand_keywords, then brand_name.
    query_candidates: List[str] = [
        (effective.get("search_query") or "").strip(),
        (effective.get("brand_keywords") or "").strip(),
        (effective.get("brand_name") or "").strip(),
    ]
    # Pick the first non-empty value.
    query = next((q for q in query_candidates if q), None)

    if not query:
        logger.error("No search_query, brand_keywords, or brand_name configured; nothing to query.")
        return

    logger.info("Starting ingestion from all sources for query: %s", query)

    # 2) Fetch raw mentions from all sources (already normalized into simple dicts).
    articles = await aggregate_all_sources(query)
    if not articles:
        logger.info("No mentions returned from any source; nothing to ingest.")
        return

    db = SessionLocal()
    created_count = 0

    try:
        # 3) For each article: enrich with sentiment + topic and build a Mention row.
        for item in articles:
            # Safely extract the text content we want to analyze.
            content = (item.get("content") or "").strip()
            if not content:
                # Skip empty items instead of inserting junk rows.
                continue

            # Run sentiment analysis (positive / negative / neutral + confidence).
            sentiment_result = await analyze_sentiment(content)

            # Infer a simple topic label using the clustering stub.
            topic = await get_topic_for_mention(content)

            # Parse created_at from NewsAPI (ISO8601) if available; fall back to now.
            created_at_raw = item.get("created_at")
            if created_at_raw:
                try:
                    created_at = isoparse(created_at_raw)
                except Exception:
                    created_at = datetime.utcnow()
            else:
                created_at = datetime.utcnow()

            # Create the ORM object; this is what will be written to PostgreSQL.
            db_mention = Mention(
                source=item.get("source") or "news",
                url=item.get("url") or "",
                author=item.get("author") or "Unknown",
                content=content,
                sentiment=sentiment_result["sentiment"],
                sentiment_score=sentiment_result["confidence"],
                topic=topic,
                created_at=created_at,
            )

            db.add(db_mention)
            created_count += 1

        # 4) Persist all new mentions in a single transaction and then
        #    run simple alert checks (spikes + negative sentiment).
        if created_count:
            db.commit()
            await run_basic_alert_checks(db)
        logger.info("Ingested %d mentions into the database", created_count)

    except Exception as exc:
        db.rollback()
        logger.error("Error during news ingestion: %s", str(exc))
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # Entry point when you run: ``python news_ingest.py``.
    # We simply run the async ingestion coroutine once and exit.
    asyncio.run(ingest_news_mentions())

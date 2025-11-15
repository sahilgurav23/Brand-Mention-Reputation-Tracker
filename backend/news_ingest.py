"""One-off script to ingest news articles into the mentions table.

Usage (from backend folder, with venv active):

    python news_ingest.py

This will:
- Read brand search settings from app.utils.config.settings
- Call NewsAPI via app.services.aggregator.aggregate_from_news
- Run sentiment + topic classification for each article
- Insert rows into the mentions table
"""

import asyncio
from datetime import datetime
from typing import List

from dateutil.parser import isoparse

from app.models.database import Mention, SessionLocal
from app.services.aggregator import aggregate_from_news
from app.services.clustering import get_topic_for_mention
from app.services.sentiment import analyze_sentiment
from app.utils.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


async def ingest_news_mentions() -> None:
    """Fetch news articles for the configured brand and store them as mentions."""

    query_candidates: List[str] = [
        settings.search_query.strip() if settings.search_query else "",
        settings.brand_keywords.strip() if settings.brand_keywords else "",
        settings.brand_name.strip() if settings.brand_name else "",
    ]
    query = next((q for q in query_candidates if q), None)

    if not query:
        logger.error("No search_query, brand_keywords, or brand_name configured; nothing to query.")
        return

    logger.info("Starting NewsAPI ingestion for query: %s", query)

    articles = await aggregate_from_news(query)
    if not articles:
        logger.info("No articles returned from NewsAPI; nothing to ingest.")
        return

    db = SessionLocal()
    created_count = 0

    try:
        for item in articles:
            content = (item.get("content") or "").strip()
            if not content:
                continue

            # Run sentiment analysis
            sentiment_result = await analyze_sentiment(content)

            # Get topic
            topic = await get_topic_for_mention(content)

            # Parse created_at from NewsAPI (ISO8601) if available
            created_at_raw = item.get("created_at")
            if created_at_raw:
                try:
                    created_at = isoparse(created_at_raw)
                except Exception:
                    created_at = datetime.utcnow()
            else:
                created_at = datetime.utcnow()

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

        if created_count:
            db.commit()
        logger.info("Ingested %d news mentions into the database", created_count)

    except Exception as exc:
        db.rollback()
        logger.error("Error during news ingestion: %s", str(exc))
        raise
    finally:
        db.close()


if __name__ == "__main__":
    asyncio.run(ingest_news_mentions())

"""Simple API endpoint to trigger ingestion from the dashboard.

This lets the frontend call a single endpoint to pull fresh mentions
from all sources (NewsAPI, Twitter, Reddit) using the same logic as
`python news_ingest.py`.
"""
from fastapi import APIRouter, HTTPException

from app.utils.logger import setup_logger
from news_ingest import ingest_news_mentions

logger = setup_logger(__name__)

router = APIRouter()


@router.post("/run")
async def run_ingestion():
    """Run the ingestion pipeline once.

    This calls the same coroutine that the `news_ingest.py` script uses.
    It is intended for development/local usage and simple dashboards,
    not for high-frequency production scheduling.
    """

    try:
        await ingest_news_mentions()
        return {"status": "ok"}
    except Exception as exc:
        logger.error("Ingestion failed via API: %s", str(exc))
        raise HTTPException(status_code=500, detail="Ingestion failed")

"""
Analytics API endpoints
"""
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.database import Mention, get_db
from app.models.schemas import SentimentDistribution, AnalyticsResponse
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


@router.get("/sentiment")
async def get_sentiment_distribution(
    db: Session = Depends(get_db),
    days: int = Query(7, description="Number of days"),
):
    """
    Get sentiment distribution for mentions
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    results = (
        db.query(Mention.sentiment, func.count(Mention.id))
        .filter(Mention.created_at >= cutoff_date)
        .group_by(Mention.sentiment)
        .all()
    )

    distribution = {"positive": 0, "negative": 0, "neutral": 0}

    for sentiment, count in results:
        if sentiment in distribution:
            distribution[sentiment] = count

    total = sum(distribution.values())

    logger.info(f"Retrieved sentiment distribution for {days} days")
    return {
        **distribution,
        "total": total,
    }


@router.get("/topics")
async def get_topic_distribution(
    db: Session = Depends(get_db),
    days: int = Query(7, description="Number of days"),
    limit: int = Query(10, description="Number of top topics"),
):
    """
    Get topic distribution
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    results = (
        db.query(Mention.topic, func.count(Mention.id).label("count"))
        .filter(Mention.created_at >= cutoff_date)
        .filter(Mention.topic.isnot(None))
        .group_by(Mention.topic)
        .order_by(func.count(Mention.id).desc())
        .limit(limit)
        .all()
    )

    topics = [{"topic": topic, "count": count} for topic, count in results]

    logger.info(f"Retrieved {len(topics)} top topics")
    return {"topics": topics}


@router.get("/timeline")
async def get_mention_timeline(
    db: Session = Depends(get_db),
    days: int = Query(7, description="Number of days"),
    granularity: str = Query("day", description="Granularity: hour, day, week"),
):
    """
    Get mention timeline data
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    # Get mentions grouped by date
    results = (
        db.query(
            func.date(Mention.created_at).label("date"),
            Mention.sentiment,
            func.count(Mention.id).label("count"),
        )
        .filter(Mention.created_at >= cutoff_date)
        .group_by(func.date(Mention.created_at), Mention.sentiment)
        .order_by(func.date(Mention.created_at))
        .all()
    )

    # Format results
    timeline = {}
    for date, sentiment, count in results:
        date_str = str(date)
        if date_str not in timeline:
            timeline[date_str] = {"positive": 0, "negative": 0, "neutral": 0, "total": 0}
        timeline[date_str][sentiment] = count
        timeline[date_str]["total"] += count

    logger.info(f"Retrieved timeline for {days} days")
    return {"timeline": timeline}


@router.get("/sources")
async def get_sources_breakdown(
    db: Session = Depends(get_db),
    days: int = Query(7, description="Number of days"),
):
    """
    Get breakdown by source
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    results = (
        db.query(Mention.source, func.count(Mention.id).label("count"))
        .filter(Mention.created_at >= cutoff_date)
        .group_by(Mention.source)
        .order_by(func.count(Mention.id).desc())
        .all()
    )

    sources = [{"source": source, "count": count} for source, count in results]

    logger.info(f"Retrieved {len(sources)} sources")
    return {"sources": sources}


@router.get("/spikes")
async def detect_spikes(
    db: Session = Depends(get_db),
    days: int = Query(7, description="Number of days for baseline"),
    threshold_sigma: float = Query(2.5, description="Standard deviation threshold"),
):
    """
    Detect mention spikes
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    # Get daily mention counts
    results = (
        db.query(func.date(Mention.created_at).label("date"), func.count(Mention.id).label("count"))
        .filter(Mention.created_at >= cutoff_date)
        .group_by(func.date(Mention.created_at))
        .order_by(func.date(Mention.created_at))
        .all()
    )

    if not results:
        return {"spikes": []}

    counts = [count for _, count in results]

    # Calculate baseline statistics
    import statistics

    mean = statistics.mean(counts)
    stdev = statistics.stdev(counts) if len(counts) > 1 else 0
    threshold = mean + (threshold_sigma * stdev)

    # Find spikes
    spikes = []
    for date, count in results:
        if count > threshold:
            spike_percentage = ((count - mean) / mean * 100) if mean > 0 else 0
            spikes.append(
                {
                    "date": str(date),
                    "count": count,
                    "baseline": mean,
                    "spike_percentage": round(spike_percentage, 2),
                }
            )

    logger.info(f"Detected {len(spikes)} spikes")
    return {"spikes": spikes, "threshold": threshold, "baseline": mean}


@router.get("/summary")
async def get_analytics_summary(
    db: Session = Depends(get_db),
    days: int = Query(7, description="Number of days"),
):
    """
    Get overall analytics summary
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    # Total mentions
    total = db.query(func.count(Mention.id)).filter(Mention.created_at >= cutoff_date).scalar()

    # Sentiment distribution
    sentiment_results = (
        db.query(Mention.sentiment, func.count(Mention.id))
        .filter(Mention.created_at >= cutoff_date)
        .group_by(Mention.sentiment)
        .all()
    )

    sentiment_dist = {"positive": 0, "negative": 0, "neutral": 0}
    for sentiment, count in sentiment_results:
        if sentiment in sentiment_dist:
            sentiment_dist[sentiment] = count

    # Top sources
    top_sources = (
        db.query(Mention.source, func.count(Mention.id).label("count"))
        .filter(Mention.created_at >= cutoff_date)
        .group_by(Mention.source)
        .order_by(func.count(Mention.id).desc())
        .limit(5)
        .all()
    )

    # Top topics
    top_topics = (
        db.query(Mention.topic, func.count(Mention.id).label("count"))
        .filter(Mention.created_at >= cutoff_date)
        .filter(Mention.topic.isnot(None))
        .group_by(Mention.topic)
        .order_by(func.count(Mention.id).desc())
        .limit(5)
        .all()
    )

    logger.info(f"Generated analytics summary for {days} days")
    return {
        "total_mentions": total,
        "sentiment_distribution": sentiment_dist,
        "top_sources": [{"source": s, "count": c} for s, c in top_sources],
        "top_topics": [{"topic": t, "count": c} for t, c in top_topics],
        "date_range": {
            "start": cutoff_date.isoformat(),
            "end": datetime.utcnow().isoformat(),
        },
    }

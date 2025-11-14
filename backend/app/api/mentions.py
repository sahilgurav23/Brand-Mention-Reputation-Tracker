"""
Mentions API endpoints
"""
from typing import List, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.models.database import Mention, get_db
from app.models.schemas import MentionCreate, MentionResponse, MentionUpdate
from app.services.sentiment import analyze_sentiment
from app.services.clustering import get_topic_for_mention
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

router = APIRouter()


@router.get("", response_model=List[MentionResponse])
async def list_mentions(
    db: Session = Depends(get_db),
    source: Optional[str] = Query(None, description="Filter by source"),
    sentiment: Optional[str] = Query(None, description="Filter by sentiment"),
    topic: Optional[str] = Query(None, description="Filter by topic"),
    days: int = Query(7, description="Number of days to retrieve"),
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(100, description="Number of records to return"),
):
    """
    List all mentions with optional filters
    """
    query = db.query(Mention)

    # Apply filters
    if source:
        query = query.filter(Mention.source == source)
    if sentiment:
        query = query.filter(Mention.sentiment == sentiment)
    if topic:
        query = query.filter(Mention.topic == topic)

    # Date filter
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    query = query.filter(Mention.created_at >= cutoff_date)

    # Order by most recent
    mentions = query.order_by(Mention.created_at.desc()).offset(skip).limit(limit).all()

    logger.info(f"Retrieved {len(mentions)} mentions")
    return mentions


@router.post("", response_model=MentionResponse)
async def create_mention(
    mention: MentionCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new mention and analyze sentiment
    """
    try:
        # Analyze sentiment
        sentiment_result = await analyze_sentiment(mention.content)

        # Get topic
        topic = await get_topic_for_mention(mention.content)

        # Create mention record
        db_mention = Mention(
            source=mention.source,
            url=mention.url,
            author=mention.author,
            content=mention.content,
            sentiment=sentiment_result["sentiment"],
            sentiment_score=sentiment_result["confidence"],
            topic=topic,
        )

        db.add(db_mention)
        db.commit()
        db.refresh(db_mention)

        logger.info(f"Created mention {db_mention.id} from {mention.source}")
        return db_mention

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating mention: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{mention_id}", response_model=MentionResponse)
async def get_mention(
    mention_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific mention by ID
    """
    mention = db.query(Mention).filter(Mention.id == mention_id).first()

    if not mention:
        raise HTTPException(status_code=404, detail="Mention not found")

    return mention


@router.put("/{mention_id}", response_model=MentionResponse)
async def update_mention(
    mention_id: int,
    mention_update: MentionUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a mention
    """
    mention = db.query(Mention).filter(Mention.id == mention_id).first()

    if not mention:
        raise HTTPException(status_code=404, detail="Mention not found")

    if mention_update.sentiment:
        mention.sentiment = mention_update.sentiment
    if mention_update.topic:
        mention.topic = mention_update.topic

    db.commit()
    db.refresh(mention)

    logger.info(f"Updated mention {mention_id}")
    return mention


@router.delete("/{mention_id}")
async def delete_mention(
    mention_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a mention
    """
    mention = db.query(Mention).filter(Mention.id == mention_id).first()

    if not mention:
        raise HTTPException(status_code=404, detail="Mention not found")

    db.delete(mention)
    db.commit()

    logger.info(f"Deleted mention {mention_id}")
    return {"message": "Mention deleted successfully"}


@router.get("/stats/sources", response_model=dict)
async def get_sources_stats(
    db: Session = Depends(get_db),
    days: int = Query(7, description="Number of days"),
):
    """
    Get statistics by source
    """
    cutoff_date = datetime.utcnow() - timedelta(days=days)

    results = (
        db.query(Mention.source, Mention.sentiment)
        .filter(Mention.created_at >= cutoff_date)
        .all()
    )

    stats = {}
    for source, sentiment in results:
        if source not in stats:
            stats[source] = {"positive": 0, "negative": 0, "neutral": 0, "total": 0}
        stats[source][sentiment] = stats[source].get(sentiment, 0) + 1
        stats[source]["total"] += 1

    return stats

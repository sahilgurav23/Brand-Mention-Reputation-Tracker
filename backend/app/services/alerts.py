"""
Alert detection and management service
"""
from datetime import datetime, timedelta
from typing import List, Dict

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.database import Mention, Alert
from app.utils.logger import setup_logger

logger = setup_logger(__name__)


async def detect_spikes(
    db: Session,
    threshold_sigma: float = 2.5,
    window_hours: int = 24,
) -> List[Dict]:
    """
    Detect mention spikes
    
    Args:
        db: Database session
        threshold_sigma: Standard deviation threshold
        window_hours: Time window in hours
        
    Returns:
        List of detected spikes
    """
    try:
        cutoff_date = datetime.utcnow() - timedelta(hours=window_hours)

        # Get hourly mention counts
        results = (
            db.query(
                func.date_trunc("hour", Mention.created_at).label("hour"),
                func.count(Mention.id).label("count"),
            )
            .filter(Mention.created_at >= cutoff_date)
            .group_by(func.date_trunc("hour", Mention.created_at))
            .order_by(func.date_trunc("hour", Mention.created_at))
            .all()
        )

        if not results:
            return []

        counts = [count for _, count in results]

        # Calculate statistics
        import statistics

        mean = statistics.mean(counts)
        stdev = statistics.stdev(counts) if len(counts) > 1 else 0
        threshold = mean + (threshold_sigma * stdev)

        # Find spikes
        spikes = []
        for hour, count in results:
            if count > threshold:
                spike_percentage = ((count - mean) / mean * 100) if mean > 0 else 0
                spikes.append(
                    {
                        "timestamp": hour,
                        "count": count,
                        "baseline": mean,
                        "spike_percentage": spike_percentage,
                    }
                )

        logger.info(f"Detected {len(spikes)} spikes")
        return spikes

    except Exception as e:
        logger.error(f"Error detecting spikes: {str(e)}")
        return []


async def detect_sentiment_shift(
    db: Session,
    window_hours: int = 24,
) -> Dict:
    """
    Detect sentiment shifts
    
    Args:
        db: Database session
        window_hours: Time window in hours
        
    Returns:
        Sentiment shift information
    """
    try:
        cutoff_date = datetime.utcnow() - timedelta(hours=window_hours)

        # Get sentiment distribution
        results = (
            db.query(Mention.sentiment, func.count(Mention.id).label("count"))
            .filter(Mention.created_at >= cutoff_date)
            .group_by(Mention.sentiment)
            .all()
        )

        sentiment_dist = {"positive": 0, "negative": 0, "neutral": 0}
        for sentiment, count in results:
            if sentiment in sentiment_dist:
                sentiment_dist[sentiment] = count

        total = sum(sentiment_dist.values())

        if total == 0:
            return {"shift": None, "distribution": sentiment_dist}

        # Calculate percentages
        percentages = {k: (v / total * 100) for k, v in sentiment_dist.items()}

        # Determine if there's a significant shift
        negative_percentage = percentages.get("negative", 0)
        if negative_percentage > 50:
            shift = "negative"
        elif negative_percentage < 20:
            shift = "positive"
        else:
            shift = "neutral"

        logger.info(f"Sentiment shift detected: {shift}")
        return {
            "shift": shift,
            "distribution": sentiment_dist,
            "percentages": percentages,
        }

    except Exception as e:
        logger.error(f"Error detecting sentiment shift: {str(e)}")
        return {"shift": None, "distribution": {}}


async def create_spike_alert(
    db: Session,
    spike_data: Dict,
) -> Alert:
    """
    Create an alert for detected spike
    
    Args:
        db: Database session
        spike_data: Spike information
        
    Returns:
        Created alert
    """
    try:
        alert = Alert(
            alert_type="spike",
            title=f"Mention Spike Detected",
            description=f"Detected {spike_data['spike_percentage']:.1f}% spike in mentions",
            severity="high" if spike_data["spike_percentage"] > 100 else "medium",
        )

        db.add(alert)
        db.commit()
        db.refresh(alert)

        logger.info(f"Created spike alert {alert.id}")
        return alert

    except Exception as e:
        db.rollback()
        logger.error(f"Error creating spike alert: {str(e)}")
        return None

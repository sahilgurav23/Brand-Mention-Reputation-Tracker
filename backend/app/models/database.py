"""
SQLAlchemy database models
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.utils.config import settings

Base = declarative_base()


class Mention(Base):
    """Mention model"""

    __tablename__ = "mentions"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String(50), index=True)  # twitter, reddit, news, blog, etc.
    url = Column(Text)
    author = Column(String(100))
    content = Column(Text)
    sentiment = Column(String(20), index=True)  # positive, negative, neutral
    sentiment_score = Column(Float)  # 0-1 confidence score
    topic = Column(String(100), index=True)
    embedding = Column(String)  # JSON string of embedding vector
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        Index("idx_source_created_at", "source", "created_at"),
        Index("idx_sentiment_created_at", "sentiment", "created_at"),
        Index("idx_topic_created_at", "topic", "created_at"),
    )


class Alert(Base):
    """Alert model"""

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_type = Column(String(50), index=True)  # spike, trend, sentiment_shift
    title = Column(String(255))
    description = Column(Text)
    severity = Column(String(20))  # low, medium, high, critical
    is_active = Column(Integer, default=1, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    resolved_at = Column(DateTime, nullable=True)


class AlertConfig(Base):
    """Alert configuration model"""

    __tablename__ = "alert_configs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    alert_type = Column(String(50))  # spike, trend, sentiment_shift
    threshold = Column(Float)
    window_hours = Column(Integer)
    is_enabled = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)


class AnalyticsCache(Base):
    """Analytics cache model for performance"""

    __tablename__ = "analytics_cache"

    id = Column(Integer, primary_key=True, index=True)
    cache_key = Column(String(255), unique=True, index=True)
    cache_value = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, index=True)


# Database connection setup
from sqlalchemy import create_engine

engine = create_engine(
    settings.database_url,
    poolclass=NullPool,
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

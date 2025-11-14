"""
Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class MentionBase(BaseModel):
    """Base mention schema"""

    source: str = Field(..., description="Source of mention (twitter, reddit, news, etc.)")
    url: str = Field(..., description="URL to the mention")
    author: str = Field(..., description="Author of the mention")
    content: str = Field(..., description="Content of the mention")


class MentionCreate(MentionBase):
    """Schema for creating a mention"""

    pass


class MentionUpdate(BaseModel):
    """Schema for updating a mention"""

    sentiment: Optional[str] = None
    topic: Optional[str] = None


class MentionResponse(MentionBase):
    """Schema for mention response"""

    id: int
    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    topic: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class AlertBase(BaseModel):
    """Base alert schema"""

    alert_type: str = Field(..., description="Type of alert (spike, trend, sentiment_shift)")
    title: str = Field(..., description="Alert title")
    description: str = Field(..., description="Alert description")
    severity: str = Field(..., description="Severity level (low, medium, high, critical)")


class AlertCreate(AlertBase):
    """Schema for creating an alert"""

    pass


class AlertResponse(AlertBase):
    """Schema for alert response"""

    id: int
    is_active: bool
    created_at: datetime
    resolved_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class AlertConfigBase(BaseModel):
    """Base alert config schema"""

    name: str = Field(..., description="Configuration name")
    alert_type: str = Field(..., description="Type of alert")
    threshold: float = Field(..., description="Alert threshold")
    window_hours: int = Field(..., description="Time window in hours")


class AlertConfigCreate(AlertConfigBase):
    """Schema for creating alert config"""

    pass


class AlertConfigResponse(AlertConfigBase):
    """Schema for alert config response"""

    id: int
    is_enabled: bool
    created_at: datetime

    class Config:
        from_attributes = True


class SentimentAnalysis(BaseModel):
    """Sentiment analysis result"""

    sentiment: str = Field(..., description="Sentiment label (positive, negative, neutral)")
    confidence: float = Field(..., description="Confidence score 0-1")


class TopicCluster(BaseModel):
    """Topic cluster result"""

    topic: str = Field(..., description="Topic name")
    count: int = Field(..., description="Number of mentions in cluster")
    keywords: List[str] = Field(..., description="Top keywords for topic")


class SentimentDistribution(BaseModel):
    """Sentiment distribution"""

    positive: int
    negative: int
    neutral: int
    total: int


class AnalyticsResponse(BaseModel):
    """Analytics response"""

    sentiment_distribution: SentimentDistribution
    top_topics: List[TopicCluster]
    top_sources: dict
    total_mentions: int
    date_range: dict


class SpikeAlert(BaseModel):
    """Spike alert data"""

    source: Optional[str] = None
    topic: Optional[str] = None
    current_count: int
    baseline_count: float
    spike_percentage: float
    timestamp: datetime


class HealthResponse(BaseModel):
    """Health check response"""

    status: str
    version: str

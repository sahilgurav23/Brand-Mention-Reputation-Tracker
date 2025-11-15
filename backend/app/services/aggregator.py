"""
Data aggregation service for collecting mentions from various sources
"""
import asyncio
from typing import List, Dict, Any

import requests

from app.utils.logger import setup_logger
from app.utils.config import settings

logger = setup_logger(__name__)


async def aggregate_from_twitter(query: str) -> List[Dict]:
    """
    Aggregate mentions from Twitter/X
    
    Args:
        query: Search query
        
    Returns:
        List of mentions
    """
    # TODO: Implement Twitter API integration
    logger.info(f"Aggregating from Twitter for query: {query}")
    return []


async def aggregate_from_reddit(query: str) -> List[Dict]:
    """
    Aggregate mentions from Reddit
    
    Args:
        query: Search query
        
    Returns:
        List of mentions
    """
    # TODO: Implement Reddit API integration
    logger.info(f"Aggregating from Reddit for query: {query}")
    return []


async def aggregate_from_news(query: str) -> List[Dict[str, Any]]:
    """
    Aggregate mentions from news sources
    
    Args:
        query: Search query
        
    Returns:
        List of normalized mention dicts with keys:
        source, url, author, content, created_at
    """

    api_key = settings.news_api_key
    if not api_key:
        logger.warning("News API key is not configured; skipping news aggregation")
        return []

    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 50,
        "apiKey": api_key,
    }

    url = "https://newsapi.org/v2/everything"
    logger.info("Fetching news articles from NewsAPI for query: %s", query)

    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        articles = data.get("articles", [])
        mentions: List[Dict[str, Any]] = []

        for art in articles:
            title = art.get("title") or ""
            description = art.get("description") or ""
            content = art.get("content") or ""
            full_content = " ".join(part for part in [title, description, content] if part).strip()

            if not full_content:
                continue

            mentions.append(
                {
                    "source": "news",
                    "url": art.get("url") or "",
                    "author": art.get("author") or (art.get("source", {}) or {}).get("name", ""),
                    "content": full_content,
                    "created_at": art.get("publishedAt"),
                }
            )

        logger.info("Fetched %d news articles from NewsAPI", len(mentions))
        return mentions

    except Exception as exc:
        logger.error("Error while fetching from NewsAPI: %s", str(exc))
        return []


async def aggregate_from_blogs(query: str) -> List[Dict]:
    """
    Aggregate mentions from blogs
    
    Args:
        query: Search query
        
    Returns:
        List of mentions
    """
    # TODO: Implement blog RSS feed integration
    logger.info(f"Aggregating from blogs for query: {query}")
    return []


async def aggregate_all_sources(query: str) -> List[Dict]:
    """
    Aggregate mentions from all sources
    
    Args:
        query: Search query
        
    Returns:
        List of mentions from all sources
    """
    logger.info(f"Starting aggregation for query: {query}")

    # Run all aggregators concurrently
    results = await asyncio.gather(
        aggregate_from_twitter(query),
        aggregate_from_reddit(query),
        aggregate_from_news(query),
        aggregate_from_blogs(query),
    )

    # Flatten results
    all_mentions = []
    for source_mentions in results:
        all_mentions.extend(source_mentions)

    logger.info(f"Aggregated {len(all_mentions)} mentions from all sources")
    return all_mentions

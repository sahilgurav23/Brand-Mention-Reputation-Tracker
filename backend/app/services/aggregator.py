"""
Data aggregation service for collecting mentions from various sources
"""
import asyncio
from datetime import datetime
from typing import List, Dict, Any

import requests

from app.utils.logger import setup_logger
from app.utils.config import settings

logger = setup_logger(__name__)


async def aggregate_from_twitter(query: str) -> List[Dict]:
    """
    Aggregate mentions from Twitter/X

    Normalizes tweets into dicts with keys: source, url, author, content, created_at.
    """

    api_key = settings.twitter_api_key
    api_secret = settings.twitter_api_secret

    if not api_key or not api_secret:
        logger.info("Twitter API credentials not configured; skipping Twitter aggregation")
        return []

    logger.info("Aggregating from Twitter for query: %s", query)

    # Step 1: obtain a bearer token using application-only auth.
    try:
        token_resp = requests.post(
            "https://api.twitter.com/oauth2/token",
            auth=(api_key, api_secret),
            data={"grant_type": "client_credentials"},
            timeout=10,
        )
        token_resp.raise_for_status()
        token_data = token_resp.json()
        bearer = token_data.get("access_token")
        if not bearer:
            logger.error("Twitter auth succeeded but no access_token was returned")
            return []
    except Exception as exc:
        logger.error("Error obtaining Twitter bearer token: %s", str(exc))
        return []

    # Step 2: call the search API for recent tweets about the query.
    search_url = "https://api.twitter.com/1.1/search/tweets.json"
    params = {
        "q": query,
        "lang": "en",
        "result_type": "recent",
        "count": 50,
    }
    headers = {"Authorization": f"Bearer {bearer}"}

    try:
        resp = requests.get(search_url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        logger.error("Error while fetching from Twitter API: %s", str(exc))
        return []

    statuses = data.get("statuses", [])
    mentions: List[Dict] = []

    for tw in statuses:
        text = (tw.get("text") or "").strip()
        if not text:
            continue

        user = tw.get("user") or {}
        tweet_id = tw.get("id_str") or ""
        created_at = tw.get("created_at")

        mentions.append(
            {
                "source": "twitter",
                "url": f"https://twitter.com/i/web/status/{tweet_id}" if tweet_id else "",
                "author": user.get("screen_name") or "",
                "content": text,
                "created_at": created_at,
            }
        )

    logger.info("Fetched %d tweets from Twitter", len(mentions))
    return mentions


async def aggregate_from_reddit(query: str) -> List[Dict]:
    """
    Aggregate mentions from Reddit

    Uses Reddit's OAuth API with the configured client ID/secret and
    normalizes posts into dicts with keys: source, url, author, content, created_at.
    """

    client_id = settings.reddit_client_id
    client_secret = settings.reddit_client_secret

    if not client_id or not client_secret:
        logger.info("Reddit API credentials not configured; skipping Reddit aggregation")
        return []

    logger.info("Aggregating from Reddit for query: %s", query)

    auth = (client_id, client_secret)
    data = {"grant_type": "client_credentials"}
    headers = {"User-Agent": "brand-tracker/0.1"}

    try:
        token_resp = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=auth,
            data=data,
            headers=headers,
            timeout=10,
        )
        token_resp.raise_for_status()
        token_data = token_resp.json()
        access_token = token_data.get("access_token")
        if not access_token:
            logger.error("Reddit auth succeeded but no access_token was returned")
            return []
    except Exception as exc:
        logger.error("Error obtaining Reddit access token: %s", str(exc))
        return []

    search_headers = {
        "Authorization": f"bearer {access_token}",
        "User-Agent": "brand-tracker/0.1",
    }
    params = {"q": query, "limit": 50, "sort": "new", "t": "week"}

    try:
        resp = requests.get(
            "https://oauth.reddit.com/search",
            headers=search_headers,
            params=params,
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        logger.error("Error while fetching from Reddit API: %s", str(exc))
        return []

    children = (data.get("data") or {}).get("children", [])
    mentions: List[Dict] = []

    for child in children:
        post = child.get("data") or {}
        text = (post.get("selftext") or post.get("title") or "").strip()
        if not text:
            continue

        created_utc = post.get("created_utc")
        created_iso: str | None
        if isinstance(created_utc, (int, float)):
            created_iso = datetime.utcfromtimestamp(created_utc).isoformat()
        else:
            created_iso = None

        mentions.append(
            {
                "source": "reddit",
                "url": f"https://www.reddit.com{post.get('permalink', '')}",
                "author": post.get("author") or "",
                "content": text,
                "created_at": created_iso,
            }
        )

    logger.info("Fetched %d posts from Reddit", len(mentions))
    return mentions


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

# Data Integration Guide

How to integrate free data sources into the Brand Mention Tracker.

## 🆓 Free Data Sources

### 1. Twitter/X API (Free Tier)

**Sign up:** https://developer.twitter.com/

**Free tier includes:**
- 450,000 tweets/month
- Real-time search
- Tweet metrics

**Implementation:**

```python
# backend/app/services/twitter_source.py

import tweepy
from app.utils.config import settings

def get_twitter_client():
    client = tweepy.Client(
        bearer_token=settings.twitter_api_key,
        wait_on_rate_limit=True
    )
    return client

async def fetch_twitter_mentions(query: str, max_results: int = 100):
    """Fetch mentions from Twitter"""
    client = get_twitter_client()
    
    tweets = client.search_recent_tweets(
        query=query,
        max_results=max_results,
        tweet_fields=['created_at', 'author_id', 'public_metrics']
    )
    
    mentions = []
    for tweet in tweets.data:
        mentions.append({
            'source': 'twitter',
            'url': f'https://twitter.com/i/web/status/{tweet.id}',
            'author': tweet.author_id,
            'content': tweet.text,
            'created_at': tweet.created_at
        })
    
    return mentions
```

**Add to requirements.txt:**
```
tweepy==4.14.0
```

---

### 2. Reddit API (Free)

**Sign up:** https://www.reddit.com/prefs/apps

**Free tier includes:**
- Unlimited API calls
- Real-time subreddit data
- Search functionality

**Implementation:**

```python
# backend/app/services/reddit_source.py

import praw
from app.utils.config import settings

def get_reddit_client():
    reddit = praw.Reddit(
        client_id=settings.reddit_client_id,
        client_secret=settings.reddit_client_secret,
        user_agent='BrandTracker/1.0'
    )
    return reddit

async def fetch_reddit_mentions(query: str, subreddits: list = None):
    """Fetch mentions from Reddit"""
    reddit = get_reddit_client()
    
    if subreddits is None:
        subreddits = ['all']
    
    mentions = []
    
    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        
        for submission in subreddit.search(query, time_filter='week', limit=50):
            mentions.append({
                'source': 'reddit',
                'url': f'https://reddit.com{submission.permalink}',
                'author': submission.author.name if submission.author else 'deleted',
                'content': submission.title + ' ' + submission.selftext,
                'created_at': submission.created_utc
            })
    
    return mentions
```

**Add to requirements.txt:**
```
praw==7.7.0
```

---

### 3. NewsAPI (Free Tier)

**Sign up:** https://newsapi.org/

**Free tier includes:**
- 100 requests/day
- News from 50,000+ sources
- Search by keyword

**Implementation:**

```python
# backend/app/services/news_source.py

import aiohttp
from app.utils.config import settings

async def fetch_news_mentions(query: str, max_results: int = 50):
    """Fetch mentions from news sources"""
    
    url = 'https://newsapi.org/v2/everything'
    
    params = {
        'q': query,
        'sortBy': 'publishedAt',
        'pageSize': max_results,
        'apiKey': settings.news_api_key
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            data = await response.json()
    
    mentions = []
    for article in data.get('articles', []):
        mentions.append({
            'source': 'news',
            'url': article['url'],
            'author': article.get('author', 'Unknown'),
            'content': article['title'] + ' ' + article.get('description', ''),
            'created_at': article['publishedAt']
        })
    
    return mentions
```

**Add to requirements.txt:**
```
aiohttp==3.9.1
```

---

### 4. RSS Feeds (Completely Free)

**No signup needed!** Use any RSS feed.

**Popular sources:**
- Tech blogs: TechCrunch, Medium, Dev.to
- News: BBC, CNN, Reuters
- Industry-specific feeds

**Implementation:**

```python
# backend/app/services/rss_source.py

import feedparser
from datetime import datetime

async def fetch_rss_mentions(feed_urls: list):
    """Fetch mentions from RSS feeds"""
    
    mentions = []
    
    for feed_url in feed_urls:
        feed = feedparser.parse(feed_url)
        
        for entry in feed.entries[:50]:  # Last 50 entries
            mentions.append({
                'source': 'blog',
                'url': entry.get('link', ''),
                'author': entry.get('author', 'Unknown'),
                'content': entry.get('title', '') + ' ' + entry.get('summary', ''),
                'created_at': entry.get('published', datetime.now().isoformat())
            })
    
    return mentions
```

**Add to requirements.txt:**
```
feedparser==6.0.10
```

---

## 🔧 Integration Steps

### Step 1: Add API Keys to `.env`

```env
# Twitter
TWITTER_API_KEY=your_bearer_token

# Reddit
REDDIT_CLIENT_ID=your_client_id
REDDIT_CLIENT_SECRET=your_client_secret

# News
NEWS_API_KEY=your_api_key

# RSS Feeds (comma-separated)
RSS_FEEDS=https://techcrunch.com/feed/,https://dev.to/feed
```

### Step 2: Create Aggregation Endpoint

```python
# backend/app/api/aggregation.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db
from app.services.twitter_source import fetch_twitter_mentions
from app.services.reddit_source import fetch_reddit_mentions
from app.services.news_source import fetch_news_mentions
from app.services.rss_source import fetch_rss_mentions
from app.api.mentions import create_mention

router = APIRouter()

@router.post("/aggregate")
async def aggregate_mentions(
    query: str,
    sources: list = ["twitter", "reddit", "news", "rss"],
    db: Session = Depends(get_db)
):
    """Aggregate mentions from multiple sources"""
    
    all_mentions = []
    
    if "twitter" in sources:
        twitter_mentions = await fetch_twitter_mentions(query)
        all_mentions.extend(twitter_mentions)
    
    if "reddit" in sources:
        reddit_mentions = await fetch_reddit_mentions(query)
        all_mentions.extend(reddit_mentions)
    
    if "news" in sources:
        news_mentions = await fetch_news_mentions(query)
        all_mentions.extend(news_mentions)
    
    if "rss" in sources:
        rss_mentions = await fetch_rss_mentions([...])
        all_mentions.extend(rss_mentions)
    
    # Save to database
    saved_mentions = []
    for mention in all_mentions:
        saved = await create_mention(mention, db)
        saved_mentions.append(saved)
    
    return {
        "total": len(saved_mentions),
        "mentions": saved_mentions
    }
```

### Step 3: Add to Main App

```python
# backend/app/main.py

from app.api import aggregation

app.include_router(aggregation.router, prefix="/api/aggregation", tags=["aggregation"])
```

### Step 4: Test Integration

```bash
# Start backend
python -m uvicorn app.main:app --reload

# Test aggregation
curl -X POST "http://localhost:8000/api/aggregation?query=your_brand&sources=twitter,reddit,news"
```

---

## 📊 Complete Integration Example

**Create a scheduled aggregation job:**

```python
# backend/app/services/scheduler.py

import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.api.aggregation import aggregate_mentions

scheduler = AsyncIOScheduler()

async def scheduled_aggregation():
    """Run aggregation every hour"""
    await aggregate_mentions(
        query="your_brand_name",
        sources=["twitter", "reddit", "news", "rss"]
    )

def start_scheduler():
    scheduler.add_job(
        scheduled_aggregation,
        'interval',
        hours=1,
        id='brand_aggregation'
    )
    scheduler.start()
```

**Add to requirements.txt:**
```
apscheduler==3.10.4
```

---

## 🎯 Quick Start: Add One Source

### Easiest: RSS Feeds (No API Key Needed)

1. **Update `.env`:**
```env
RSS_FEEDS=https://techcrunch.com/feed/,https://dev.to/feed
```

2. **Add to requirements.txt:**
```
feedparser==6.0.10
```

3. **Create `backend/app/services/rss_source.py`** (see above)

4. **Test:**
```bash
cd backend
pip install feedparser
python -c "
import asyncio
from app.services.rss_source import fetch_rss_mentions

feeds = ['https://techcrunch.com/feed/']
mentions = asyncio.run(fetch_rss_mentions(feeds))
print(f'Found {len(mentions)} mentions')
"
```

---

## 📈 Data Flow

```
Free Data Sources
    ↓
Aggregation Service
    ↓
Sentiment Analysis
    ↓
Topic Clustering
    ↓
Database Storage
    ↓
Dashboard Display
```

---

## 💡 Tips

1. **Start with RSS** - No API key needed
2. **Add Twitter next** - Free tier is generous
3. **Use Reddit** - Unlimited API calls
4. **Add News** - 100 requests/day is enough for testing
5. **Schedule jobs** - Run aggregation hourly/daily

---

## 🔗 Useful Links

- **Twitter API**: https://developer.twitter.com/
- **Reddit API**: https://www.reddit.com/prefs/apps
- **NewsAPI**: https://newsapi.org/
- **RSS Feeds**: https://www.rss-feeds.com/
- **APScheduler**: https://apscheduler.readthedocs.io/

---

**Start with RSS feeds - they're the easiest!** 🚀

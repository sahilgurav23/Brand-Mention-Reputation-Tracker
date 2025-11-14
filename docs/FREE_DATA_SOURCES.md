# Free Data Sources

Quick comparison of free data sources for brand mention tracking.

## 📊 Comparison Table

| Source | Cost | Requests/Month | Signup | Difficulty |
|--------|------|----------------|--------|-----------|
| **RSS Feeds** | Free | Unlimited | No | ⭐ Easy |
| **Twitter API** | Free | 450,000 | Yes | ⭐⭐ Medium |
| **Reddit API** | Free | Unlimited | Yes | ⭐⭐ Medium |
| **NewsAPI** | Free | 3,000 | Yes | ⭐⭐ Medium |
| **HackerNews API** | Free | Unlimited | No | ⭐ Easy |
| **YouTube API** | Free | 10,000/day | Yes | ⭐⭐⭐ Hard |

---

## 🆓 Best Free Options

### 1. RSS Feeds ⭐⭐⭐ (RECOMMENDED)

**Why:** No signup, unlimited, easy to implement

**Popular feeds:**
```
TechCrunch: https://techcrunch.com/feed/
Medium: https://medium.com/feed/tag/[topic]
Dev.to: https://dev.to/feed
HackerNews: https://news.ycombinator.com/rss
Reddit: https://www.reddit.com/r/[subreddit]/new/.rss
```

**Setup time:** 5 minutes

---

### 2. Twitter API ⭐⭐

**Why:** Real-time, large volume, free tier is good

**Limits:** 450,000 tweets/month

**Setup time:** 15 minutes

**Get key:** https://developer.twitter.com/

---

### 3. Reddit API ⭐⭐

**Why:** Unlimited, easy to use, active communities

**Limits:** Unlimited

**Setup time:** 10 minutes

**Get key:** https://www.reddit.com/prefs/apps

---

### 4. NewsAPI ⭐⭐

**Why:** Professional news sources, good coverage

**Limits:** 100 requests/day (3,000/month)

**Setup time:** 10 minutes

**Get key:** https://newsapi.org/

---

### 5. HackerNews API ⭐⭐⭐

**Why:** No signup, unlimited, tech-focused

**Limits:** Unlimited

**Setup time:** 5 minutes

**Docs:** https://github.com/HackerNews/API

---

## 🚀 Quick Start (5 minutes)

### Step 1: Choose a Source

Start with **RSS Feeds** (easiest):

```python
# No API key needed!
feed_urls = [
    'https://techcrunch.com/feed/',
    'https://dev.to/feed',
    'https://news.ycombinator.com/rss'
]
```

### Step 2: Install Library

```bash
pip install feedparser
```

### Step 3: Fetch Data

```python
import feedparser

feed = feedparser.parse('https://techcrunch.com/feed/')

for entry in feed.entries[:10]:
    print(f"Title: {entry.title}")
    print(f"Link: {entry.link}")
    print(f"Summary: {entry.summary}\n")
```

### Step 4: Add to Backend

See [DATA_INTEGRATION_GUIDE.md](./DATA_INTEGRATION_GUIDE.md)

---

## 📝 Implementation Order

1. **Week 1:** Add RSS feeds (easiest)
2. **Week 2:** Add Reddit API (unlimited)
3. **Week 3:** Add Twitter API (real-time)
4. **Week 4:** Add NewsAPI (professional sources)

---

## 💰 Cost Breakdown

| Source | Monthly Cost | Notes |
|--------|------------|-------|
| RSS Feeds | $0 | Unlimited |
| Twitter API | $0 | 450K tweets/month free |
| Reddit API | $0 | Unlimited |
| NewsAPI | $0 | 100 requests/day free |
| HackerNews API | $0 | Unlimited |
| **TOTAL** | **$0** | All free! |

---

## ⚡ Easiest Implementation

### Option 1: RSS Only (5 minutes)

```python
import feedparser

async def get_mentions(brand_name):
    feeds = [
        'https://techcrunch.com/feed/',
        'https://dev.to/feed'
    ]
    
    mentions = []
    for feed_url in feeds:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            if brand_name.lower() in entry.title.lower():
                mentions.append({
                    'source': 'blog',
                    'url': entry.link,
                    'author': entry.get('author', 'Unknown'),
                    'content': entry.title,
                    'created_at': entry.published
                })
    
    return mentions
```

### Option 2: RSS + Reddit (15 minutes)

```python
import feedparser
import praw

async def get_mentions(brand_name):
    # RSS
    rss_mentions = await get_rss_mentions(brand_name)
    
    # Reddit
    reddit = praw.Reddit(...)
    reddit_mentions = await get_reddit_mentions(brand_name, reddit)
    
    return rss_mentions + reddit_mentions
```

---

## 🎯 Recommended Setup

**For MVP:**
1. RSS Feeds (start immediately)
2. Reddit API (add next)

**For Production:**
1. RSS Feeds
2. Reddit API
3. Twitter API
4. NewsAPI
5. HackerNews API

---

## 📚 Resources

- **RSS Feeds**: https://www.rss-feeds.com/
- **Twitter API**: https://developer.twitter.com/
- **Reddit API**: https://www.reddit.com/prefs/apps
- **NewsAPI**: https://newsapi.org/
- **HackerNews API**: https://github.com/HackerNews/API

---

**Start with RSS feeds - they're completely free and require no signup!** 🚀

# API Quick Reference

## Base URL
```
http://localhost:8000
```

## Mentions

```bash
# List mentions
GET /api/mentions?days=7&limit=50

# Create mention
POST /api/mentions
{
  "source": "twitter",
  "url": "...",
  "author": "...",
  "content": "..."
}

# Get mention
GET /api/mentions/{id}

# Delete mention
DELETE /api/mentions/{id}
```

## Analytics

```bash
# Sentiment distribution
GET /api/analytics/sentiment?days=7

# Topics
GET /api/analytics/topics?days=7

# Timeline
GET /api/analytics/timeline?days=7

# Sources
GET /api/analytics/sources?days=7

# Spikes
GET /api/analytics/spikes?days=7

# Summary
GET /api/analytics/summary?days=7
```

## Alerts

```bash
# List alerts
GET /api/alerts

# Create alert
POST /api/alerts
{
  "alert_type": "spike",
  "title": "...",
  "description": "...",
  "severity": "high"
}

# Resolve alert
PUT /api/alerts/{id}/resolve

# Delete alert
DELETE /api/alerts/{id}
```

## Interactive Docs

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

See [API.md](./API.md) for complete documentation.

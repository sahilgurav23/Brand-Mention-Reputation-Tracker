"""Topic clustering service (lightweight stub).

This implementation deliberately avoids importing heavy ML dependencies
like ``sentence_transformers`` and ``scikit-learn`` so that the backend
can run in constrained environments. The public function signatures are
kept the same so that other parts of the codebase do not need changes.
"""

from typing import List, Dict, Any

from app.utils.logger import setup_logger

logger = setup_logger(__name__)


async def get_topic_for_mention(text: str) -> str:
    """
    Get topic/category for a mention
    
    Args:
        text: Text to categorize
        
    Returns:
        Topic string

    Note:
        This is a stub implementation. It does *not* perform real
        clustering; it just returns a generic topic so that mention
        creation works without ML dependencies.
    """

    if not text.strip():
        return "uncategorized"

    # Very naive rule-based stub: could be improved later
    lowered = text.lower()
    if any(word in lowered for word in ["error", "bug", "issue", "problem"]):
        topic = "support"
    elif any(word in lowered for word in ["feature", "update", "release"]):
        topic = "product-updates"
    else:
        topic = "general"

    logger.debug("Assigned stub topic '%s' for text: %s", topic, text[:80])
    return topic


async def cluster_mentions(texts: List[str], n_clusters: int = 5) -> Dict[str, Any]:
    """
    Cluster mentions into topics
    
    Args:
        texts: List of mention texts
        n_clusters: Number of clusters to create
        
    Returns:
        Dictionary with cluster assignments and centers.

    Note:
        Stub implementation: each text becomes its own "cluster".
    """

    clusters: Dict[int, List[str]] = {}
    for idx, text in enumerate(texts):
        clusters[idx] = [text]

    logger.info("Stub clustering: returned %d single-item clusters", len(texts))
    return {"clusters": clusters, "centers": [], "labels": list(range(len(texts)))}


async def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Get embeddings for texts
    
    Args:
        texts: List of texts
        
    Returns:
        List of embeddings.

    Note:
        Stub implementation: returns an empty list to avoid depending on
        external ML libraries.
    """

    if not texts:
        return []

    logger.warning("Stub get_embeddings called; returning empty embeddings list")
    return []

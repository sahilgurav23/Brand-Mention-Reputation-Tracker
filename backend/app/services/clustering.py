"""
Topic clustering service
"""
from typing import List

from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans

from app.utils.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# Initialize embedding model
try:
    embedding_model = SentenceTransformer(settings.embedding_model)
    logger.info(f"Loaded embedding model: {settings.embedding_model}")
except Exception as e:
    logger.error(f"Failed to load embedding model: {str(e)}")
    embedding_model = None


async def get_topic_for_mention(text: str) -> str:
    """
    Get topic/category for a mention
    
    Args:
        text: Text to categorize
        
    Returns:
        Topic string
    """
    if not embedding_model:
        logger.warning("Embedding model not available")
        return "uncategorized"

    try:
        # Get embedding
        embedding = embedding_model.encode(text, convert_to_tensor=False)

        # For now, return a generic topic
        # In production, this would compare against known topics
        # and assign the closest match

        logger.debug(f"Generated embedding for topic classification")
        return "general"

    except Exception as e:
        logger.error(f"Error getting topic: {str(e)}")
        return "uncategorized"


async def cluster_mentions(texts: List[str], n_clusters: int = 5) -> dict:
    """
    Cluster mentions into topics
    
    Args:
        texts: List of mention texts
        n_clusters: Number of clusters to create
        
    Returns:
        Dictionary with cluster assignments and centers
    """
    if not embedding_model:
        logger.warning("Embedding model not available")
        return {"clusters": [], "centers": []}

    try:
        if len(texts) < n_clusters:
            n_clusters = max(1, len(texts) - 1)

        # Get embeddings
        embeddings = embedding_model.encode(texts, convert_to_tensor=False)

        # Cluster
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(embeddings)

        # Group texts by cluster
        clusters = {}
        for idx, label in enumerate(labels):
            if label not in clusters:
                clusters[label] = []
            clusters[label].append(texts[idx])

        logger.info(f"Clustered {len(texts)} texts into {n_clusters} topics")
        return {
            "clusters": clusters,
            "centers": kmeans.cluster_centers_.tolist(),
            "labels": labels.tolist(),
        }

    except Exception as e:
        logger.error(f"Error clustering mentions: {str(e)}")
        return {"clusters": {}, "centers": [], "labels": []}


async def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Get embeddings for texts
    
    Args:
        texts: List of texts
        
    Returns:
        List of embeddings
    """
    if not embedding_model:
        logger.warning("Embedding model not available")
        return []

    try:
        embeddings = embedding_model.encode(texts, convert_to_tensor=False)
        logger.debug(f"Generated embeddings for {len(texts)} texts")
        return embeddings.tolist()

    except Exception as e:
        logger.error(f"Error generating embeddings: {str(e)}")
        return []

"""
Sentiment analysis service
"""
from typing import Dict

from transformers import pipeline

from app.utils.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

# Initialize sentiment pipeline
try:
    sentiment_pipeline = pipeline(
        "sentiment-analysis",
        model=settings.sentiment_model,
        device=-1,  # Use CPU, set to 0 for GPU
    )
    logger.info(f"Loaded sentiment model: {settings.sentiment_model}")
except Exception as e:
    logger.error(f"Failed to load sentiment model: {str(e)}")
    sentiment_pipeline = None


async def analyze_sentiment(text: str) -> Dict[str, any]:
    """
    Analyze sentiment of text
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary with sentiment and confidence score
    """
    if not sentiment_pipeline:
        logger.warning("Sentiment pipeline not available, returning neutral")
        return {"sentiment": "neutral", "confidence": 0.5}

    try:
        # Truncate text if too long
        text = text[:512]

        result = sentiment_pipeline(text)[0]

        # Map model output to our labels
        label = result["label"].lower()
        score = result["score"]

        # Convert to our sentiment labels
        if label == "positive":
            sentiment = "positive"
        elif label == "negative":
            sentiment = "negative"
        else:
            sentiment = "neutral"

        logger.debug(f"Sentiment analysis: {sentiment} ({score:.2f})")
        return {"sentiment": sentiment, "confidence": score}

    except Exception as e:
        logger.error(f"Error analyzing sentiment: {str(e)}")
        return {"sentiment": "neutral", "confidence": 0.5}


async def batch_analyze_sentiment(texts: list) -> list:
    """
    Analyze sentiment of multiple texts
    
    Args:
        texts: List of texts to analyze
        
    Returns:
        List of sentiment analysis results
    """
    if not sentiment_pipeline:
        logger.warning("Sentiment pipeline not available")
        return [{"sentiment": "neutral", "confidence": 0.5} for _ in texts]

    try:
        # Truncate texts
        texts = [text[:512] for text in texts]

        results = sentiment_pipeline(texts)

        output = []
        for result in results:
            label = result["label"].lower()
            score = result["score"]

            if label == "positive":
                sentiment = "positive"
            elif label == "negative":
                sentiment = "negative"
            else:
                sentiment = "neutral"

            output.append({"sentiment": sentiment, "confidence": score})

        logger.debug(f"Batch sentiment analysis completed for {len(texts)} texts")
        return output

    except Exception as e:
        logger.error(f"Error in batch sentiment analysis: {str(e)}")
        return [{"sentiment": "neutral", "confidence": 0.5} for _ in texts]

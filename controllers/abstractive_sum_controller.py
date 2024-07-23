from scripts.abstractive_summarizer import abstractive_summarization
from config.logs import logger

async def abstractive_summarization_controller(text: str, style: str, compression_ratio: int) -> str:
    try:
        summary, usage = abstractive_summarization(text, style, compression_ratio)
        return summary, usage
    except Exception as e:
        logger.error(f"Error in abstractive summarization: {str(e)}")
        raise ValueError(f"Failed to generate summary: {str(e)}")
from scripts.extractive_summarizer import extractive_summarization
from config.logs import logger

async def extractive_summarization_controller(text: str, compression_ratio: int) -> str:
    try:
        logger.info("Started extractive summarization")
        summary = extractive_summarization(text, compression_ratio)
        logger.info("Extractive summarization completed")
        return summary
    except Exception as e:
        logger.error(f"Error in extractive summarization: {str(e)}")
        raise ValueError(f"Failed to generate summary: {str(e)}")
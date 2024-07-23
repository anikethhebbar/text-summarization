from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, field_validator
from controllers.abstractive_sum_controller import abstractive_summarization_controller
from controllers.extractive_sum_controller import extractive_summarization_controller
from config.logs import logger

router = APIRouter()

class AbstractiveSummarizationRequest(BaseModel):
    text: str
    style: str
    compression_ratio: int = Field(..., ge=20, le=80)

    @field_validator("compression_ratio")
    def validate_compression_ratio(cls, v):
        if v % 10 != 0:
            logger.error("ValueError: compression_ratio must be a multiple of 10")
            raise ValueError("compression_ratio must be a multiple of ten")
        return v

    @field_validator("text")
    def validate_text(cls, v):
        words = v.split()
        if len(words) < 100:
            logger.error("ValueError: text must contain at least 100 words")
            raise ValueError("text must contain at least 100 words")
        return v

class ExtractiveSummarizationRequest(BaseModel):
    text: str
    compression_ratio: int = Field(..., ge=20, le=80)

    @field_validator("compression_ratio")
    def validate_compression_ratio(cls, v):
        if v % 10 != 0:
            logger.error("ValueError: compression_ratio must be a multiple of 10")
            raise ValueError("compression_ratio must be a multiple of ten")
        return v

    @field_validator("text")
    def validate_text(cls, v):
        words = v.split()
        if len(words) < 100:
            logger.error("ValueError: text must contain at least 100 words")
            raise ValueError("text must contain at least 100 words")
        return v

@router.post("/abstractive_summarizer")
async def summarize_abstractive(request: AbstractiveSummarizationRequest):
    try:
        summary, usage = await abstractive_summarization_controller(
            request.text, request.style, request.compression_ratio
        )
        if summary is None:
            logger.error("Error: abstractive_summarization returned None")
            raise ValueError("Failed to generate summary")

        text_summary = summary[0].text if summary else None

        return {"summary": text_summary,
                "token_usage": {
                "input_tokens": usage.input_tokens,
                "output_tokens": usage.output_tokens,
                "total_tokens": usage.input_tokens + usage.output_tokens
            }}
    except Exception as e:
        logger.error(f"Error in /abstractive_summarizer endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred during summarization: {str(e)}")

@router.post("/extractive_summarizer")
async def summarize_extractive(request: ExtractiveSummarizationRequest):
    try:
        summary = await extractive_summarization_controller(
            request.text, request.compression_ratio
        )
        return {"summary": summary}
    except Exception as e:
        logger.error(f"Error in /extractive_summarizer endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred during summarization: {str(e)}")
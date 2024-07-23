import anthropic
import os
import traceback
from config.logs import logger
import json
import math
from dotenv import load_dotenv

load_dotenv()

# Retrieve the secret value
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
# Use the API key with the Anthropic library
# Use the API key with the Anthropic library
client = anthropic.Client(api_key=anthropic_api_key)

def abstractive_summarization(text, style, compression_ratio):
    try:
        len_words = len(text.split(" "))
        
        len_word_summary = math.floor(compression_ratio * len_words/100)

        logger.info("Started abstractive summarization")
        
        style_instructions = {
            "bulleted_list": "Use bullet points for each main idea or piece of information.",
            "original_style": "Maintain a style similar to the original text.",
            "concise": "Provide a brief and to-the-point summary.",
            "formal": "Use formal language and tone in the summary."
        }

        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4096,
            temperature=0.1,
            messages=[
                {
                    "role": "user",
                    #"content": f'''Text to summarize: "{text}". Summarize this text such that it MUST STRCITLY contain {len_word_summary} words in the following style: {style_instructions[style]}. Result should directly start with summary, Do not start with "here is the..."'''
                    "content": f"""Text to summarize: "{text}". Your task is to provide a summary that strictly adheres to the following guidelines:
                                    1. The summary must contain exactly {len_word_summary} words, no more, no less.
                                    2. The summary must be written in the {style_instructions[style]} style.
                                    Please ensure that your response starts directly with the summary and does not include any preamble like "here is the...". The word count of {len_word_summary} words includes every word in your response."""
                }
            ]
        )

        logger.info("Abstractive summarization completed")
        logger.info(message.usage)

        return message.content, message.usage
    except Exception as e:
        logger.error(f"Encountered the following error while abstractive summarization - {e}")
        logger.error(traceback.format_exc())
        raise Exception(f"Encountered the following error while abstractive summarization - {e}")
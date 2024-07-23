## Text Summarization using NLTK and LLMs
This project provides an API for text summarization using both extractive and abstractive methods.

## Features

- Extractive summarization
- Abstractive summarization
- Customizable compression ratio
- Multiple output styles for abstractive summarization

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/anikethhebbar/text-summarization.git
   cd text-summarization
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up the environment variables:
   - Create a `.env` file in the root directory
   - Add your Anthropic API key: `ANTHROPIC_API_KEY=your_api_key_here`

## Usage

To start the server, run:

```
uvicorn app:app --host 0.0.0.0 --port 5001
```
Or

```
python app.py
```

The API will be available at `http://localhost:5001`.

### Endpoints

1. Extractive Summarization:
   - POST `/extractive_summarizer`
   - Request body:
     ```json
     {
       "text": "Your long text here...",
       "compression_ratio": 30
     }
     ```

2. Abstractive Summarization:
   - POST `/abstractive_summarizer`
   - Request body:
     ```json
     {
       "text": "Your long text here...",
       "style": "concise",
       "compression_ratio": 30
     }
     ```

### Compression Ratio

The compression ratio determines the length of the summary relative to the original text. It should be an integer between 20 and 80, and must be a multiple of 10.

### Word Limits

- Minimum word limit: The input text must contain at least 100 words.
- Maximum word limit: There is no hard-coded maximum word limit for the input text. However, be aware of the following considerations:
  - For extractive summarization, very long texts may result in longer processing times.
  - For abstractive summarization, the Anthropic API has a maximum token limit. Very long texts may be truncated or result in an error.

### Abstractive Summarization Styles

- `bulleted_list`: Uses bullet points for each main idea.
- `original_style`: Maintains a style similar to the original text.
- `concise`: Provides a brief and to-the-point summary.
- `formal`: Uses formal language and tone in the summary.

## Docker

To run the application using Docker:

1. Build the Docker image:
   ```
   docker build -t ds-summarization-api .
   ```

2. Run the Docker container:
   ```
   docker run -p 5001:5001 -e ANTHROPIC_API_KEY=your_api_key_here ds-summarization-api
   ```

import gradio as gr
import requests
import json

API_URL = "http://localhost:5001"  # Update this with your actual API URL

def abstractive_summarize(text, style, compression_ratio):
    try:
        response = requests.post(
            f"{API_URL}/abstractive_summarizer",
            json={
                "text": text,
                "style": style,
                "compression_ratio": compression_ratio
            }
        )
        response.raise_for_status()
        result = response.json()
        summary = result["summary"]
        token_usage = result["token_usage"]
        return summary, f"Token Usage: {json.dumps(token_usage, indent=2)}"
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}", ""

def extractive_summarize(text, compression_ratio):
    try:
        response = requests.post(
            f"{API_URL}/extractive_summarizer",
            json={
                "text": text,
                "compression_ratio": compression_ratio
            }
        )
        response.raise_for_status()
        result = response.json()
        return result["summary"]
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

def validate_input(text, compression_ratio):
    if len(text.split()) < 100:
        return "Error: Text must contain at least 100 words."
    if compression_ratio % 10 != 0 or compression_ratio < 20 or compression_ratio > 80:
        return "Error: Compression ratio must be a multiple of 10 between 20 and 80."
    return None

# Load custom CSS
with open("style.css", "r") as f:
    custom_css = f.read()

with gr.Blocks(css=custom_css) as demo:
    gr.Markdown("# Text Summarization")
    
    with gr.Tab("Abstractive Summarization"):
        with gr.Row():
            with gr.Column(scale=2):
                text_input = gr.Textbox(label="Input Text", lines=10)
                style = gr.Dropdown(["bulleted_list", "original_style", "concise", "formal"], label="Summary Style")
                compression_ratio = gr.Slider(20, 80, step=10, label="Compression Ratio (%)")
                submit_button = gr.Button("Summarize")
            with gr.Column(scale=1):
                summary_output = gr.Textbox(label="Summary", lines=10)
                token_usage = gr.Textbox(label="Token Usage", lines=5)
        
        submit_button.click(
            fn=lambda text, style, ratio: (
                abstractive_summarize(text, style, ratio) 
                if validate_input(text, ratio) is None 
                else (validate_input(text, ratio), "")
            ),
            inputs=[text_input, style, compression_ratio],
            outputs=[summary_output, token_usage]
        )
    
    with gr.Tab("Extractive Summarization"):
        with gr.Row():
            with gr.Column(scale=2):
                text_input_ex = gr.Textbox(label="Input Text", lines=10)
                compression_ratio_ex = gr.Slider(20, 80, step=10, label="Compression Ratio (%)")
                submit_button_ex = gr.Button("Summarize")
            with gr.Column(scale=1):
                summary_output_ex = gr.Textbox(label="Summary", lines=10)
        
        submit_button_ex.click(
            fn=lambda text, ratio: (
                extractive_summarize(text, ratio) 
                if validate_input(text, ratio) is None 
                else validate_input(text, ratio)
            ),
            inputs=[text_input_ex, compression_ratio_ex],
            outputs=summary_output_ex
        )

if __name__ == "__main__":
    demo.launch()
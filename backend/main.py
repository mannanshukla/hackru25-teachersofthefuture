from fastapi import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
import subprocess
import os
import requests
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
# Initialize FastAPI app
app = FastAPI()

# Enable CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to your frontend URL if necessary
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directories for logs and output
OUTPUT_DIR = "output"
LOG_DIR = "logs"
OLLAMA_API_URL = "http://127.0.0.1:11434/api/generate"  # Use 127.0.0.1 for better resolution

# Ensure output & log directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(f"{LOG_DIR}/error.log"),
        logging.StreamHandler()
    ]
)

def log_ollama_response(response_text: str):
    """ Logs the full response from Ollama API """
    with open(f"{LOG_DIR}/ollama_response.log", "a") as log_file:
        log_file.write(f"\n[{datetime.now()}] Ollama Response:\n{response_text}\n\n")

class PresentationRequest(BaseModel):
    topic: str
    notes: str
    reading_level: str

@app.post("/generate_presentation/")
async def generate_presentation(data: PresentationRequest):
    """
    Generates Beamer LaTeX code using Ollama API and compiles it into a PDF.
    Logs important events and responses.
    """

    # Constructing the Ollama API request
    ollama_payload = {
        "model": "llama3.1",
        "prompt": fr"""
        Generate a clean and professional Beamer LaTeX presentation.

        **Topic:** "{data.topic}"
        **Reading Level:** {data.reading_level}
        **Required Points:** {data.notes}

        🔹 **Beamer Structure Instructions:**
        - Use `\documentclass{{beamer}}` as the document class.
        - Use `\usetheme{{Warsaw}}` for styling.
        - The title page should include:
          - `\title{{{data.topic}}}`
          - `\author{{Lee Becker-Cirelli}}`
          - `\institute{{Rutgers University}}`
          - `\date{{\today}}`
        - Ensure every slide is enclosed in `\begin{{frame}} ... \end{{frame}}`.
        - Use `\frametitle{{}}` to define each slide's title.
        - Do **NOT** include a Table of Contents.
        - Format slides clearly with bullet points, concise explanations, and **no excessive text**.
        - Ensure the LaTeX code compiles properly.

        🔹 **Beamer Sections:**
        1. **Title Page**
        2. **Introduction** – Define the topic concisely.
        3. **Main Content** – Explain key points in `{data.notes}`.
        4. **Conclusion** – Summarize key takeaways.

        Return **only** the raw Beamer LaTeX code. Do not include explanations, markdown, or extra text. NO BACKTICKS HOLY FUCKING SHIT NO BACKTICKS, JUST RAW LATEX CODE THAT NEEDS TO BE COMPILED
        """,
        "stream": False
    }

    logging.info(f"Sending request to Ollama API for topic: {data.topic}")

    # Call Ollama API
    try:
        response = requests.post(OLLAMA_API_URL, json=ollama_payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Ollama API request failed: {e}")
        return {"error": f"Failed to communicate with Ollama API: {e}"}

    # Extract LaTeX code from Ollama response
    latex_code = response.json().get("response", "").strip()

    # Log the full Ollama response
    log_ollama_response(latex_code)

    if not latex_code.startswith(r"\documentclass"):  # Sanity check
        logging.error("Invalid LaTeX output received from Ollama")
        return {"error": "Invalid LaTeX output from Ollama"}

    tex_file_path = os.path.join(OUTPUT_DIR, "presentation.tex")
    pdf_file_path = os.path.join(OUTPUT_DIR, "presentation.pdf")

    # Save LaTeX to file
    with open(tex_file_path, "w") as f:
        f.write(latex_code)
    
    logging.info(f"LaTeX file saved: {tex_file_path}")

    # Compile LaTeX to PDF using pdflatex (Non-Interactive Mode)
    compile_command = [
        "pdflatex",
        "-interaction=nonstopmode",  # Prevents waiting for user input
        "-halt-on-error",  # Stops only on fatal errors
        "-output-directory=" + OUTPUT_DIR,
        tex_file_path
    ]

    try:
        result = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        logging.info(f"PDF successfully generated: {pdf_file_path}")
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode() if e.stderr else "Unknown error"
        logging.error(f"pdflatex failed with error:\n{error_message}")
        return {"error": "Failed to compile PDF. Check LaTeX formatting."}

    # Check if PDF exists
    if not os.path.exists(pdf_file_path):
        logging.error("PDF generation failed")
        return {"error": "PDF generation failed"}

    return {"pdf_url": f"/pdf_output/presentation.pdf"}

@app.get("/pdf_output/{filename}")
async def get_pdf(filename: str):
    """
    Returns the generated PDF file as an embedded response.
    """
    file_path = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(file_path):
        logging.info(f"Serving PDF file: {file_path}")
        return FileResponse(file_path, media_type='application/pdf')
    logging.error(f"Requested PDF not found: {filename}")
    return {"error": "File not found"}

@app.get("/embed_presentation/")
async def embed_presentation():
    """
    Serves an HTML page with an embedded PDF.
    """
    pdf_url = "/pdf_output/presentation.pdf"
    return HTMLResponse(content=f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Generated Presentation</title>
        <style>
            body {{
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                background-color: #f4f4f4;
                margin: 0;
            }}
            iframe {{
                width: 80%;
                height: 90vh;
                border: none;
            }}
        </style>
    </head>
    <body>
        <iframe src="{pdf_url}" allowfullscreen></iframe>
    </body>
    </html>
    """)

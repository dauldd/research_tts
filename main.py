import os
from dotenv import load_dotenv
from scripts.fetch_pdf import fetch_pdf
from scripts.process_text import extract_text, prepare_podcast_text_gemini
from scripts.generate_audio import generate_audio

load_dotenv()
ELEVENLABS_API_KEY = os.environ['ELEVENLABS_API_KEY']
GEMINI_API_KEY = os.environ['GEMINI_API_KEY']

PDF_URL = "https://metr.org/AI_R_D_Evaluation_Report.pdf"
OUTPUT_FILE = "episodes/podcast_audio.mp3"

pdf_content = fetch_pdf(PDF_URL)
if pdf_content:
    text = extract_text(pdf_content)
    if text:
        podcast_text = prepare_podcast_text_gemini(text, GEMINI_API_KEY)
        if podcast_text:
            generate_audio(podcast_text, OUTPUT_FILE, ELEVENLABS_API_KEY)

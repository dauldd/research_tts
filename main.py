import os
import sys
from dotenv import load_dotenv
from scripts.fetch_pdf import fetch_pdf
from scripts.process_text import extract_text, prepare_podcast_text_gemini, split_script

load_dotenv()
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

OUTPUT_FILE = "episodes/podcast_audio.mp3"

if len(sys.argv) < 2:
    print("Usage: python main.py [google|elevenlabs]")
    sys.exit(1)

provider = sys.argv[1].lower()

if provider == "google":
    from scripts.generate_google import generate_audio
elif provider == "elevenlabs":
    from scripts.generate_elevenlabs import generate_audio
    ELEVENLABS_API_KEY = os.environ['ELEVENLABS_API_KEY']
else:
    print("Invalid provider. Use 'google' or 'elevenlabs'")
    sys.exit(1)

pdf_content = fetch_pdf()
if pdf_content:
    text = extract_text(pdf_content)
    if text:
        podcast_text = prepare_podcast_text_gemini(text, GOOGLE_API_KEY, False)
        if podcast_text:
            if provider == "google":
                generate_audio(podcast_text, OUTPUT_FILE)
            else:
                generate_audio(podcast_text, OUTPUT_FILE, ELEVENLABS_API_KEY)

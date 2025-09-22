import os
import sys
import re
from dotenv import load_dotenv
from scripts.fetch_pdf import fetch_pdf, parse_calendar_events, fetch_calendar_data, get_latest_event
from scripts.process_text import extract_text, prepare_podcast_text_gemini, split_script

load_dotenv()
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

def sanitize_filename(title):
    safe_title = re.sub(r'[<>:"/\\|?*]', '', title)
    safe_title = re.sub(r'\s+', '_', safe_title.strip())
    return safe_title[:50]

def get_output_filename():
    try:
        ics_content = fetch_calendar_data()
        if ics_content:
            events = parse_calendar_events(ics_content)
            latest_event = get_latest_event(events)
            if latest_event and 'title' in latest_event:
                safe_title = sanitize_filename(latest_event['title'])
                return f"episodes/{safe_title}.mp3"
    except Exception as e:
        print(f"Error getting event title: {e}")

    return "episodes/podcast_audio.mp3"

OUTPUT_FILE = get_output_filename()

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

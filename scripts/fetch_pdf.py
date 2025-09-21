import os
import re
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CALENDAR_URL = os.environ.get('CALENDAR_URL', '')

def fetch_calendar_data():
    try:
        response = requests.get(CALENDAR_URL, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching calendar: {e}")
        return ""

def parse_calendar_events(ics_content):
    events = []
    current_event = {}
    
    lines = ics_content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        if line == "BEGIN:VEVENT":
            current_event = {}
        elif line == "END:VEVENT":
            if current_event:
                events.append(current_event.copy())
        elif line.startswith("SUMMARY:"):
            current_event['title'] = line[8:]
        elif line.startswith("DESCRIPTION:"):
            description = line[12:]
            i += 1
            while i < len(lines) and lines[i].startswith(' '):
                description += lines[i][1:]
                i += 1
            i -= 1
            current_event['description'] = description
        elif line.startswith("DTSTART:") or line.startswith("DTSTART;"):
            date_part = line.split(':')[-1]
            current_event['start_date'] = date_part
        elif line.startswith("LOCATION:"):
            current_event['location'] = line[9:]
        
        i += 1
    
    return events

def extract_arxiv_urls(description):
    if not description:
        return []
    
    arxiv_pattern = r'https://arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})'
    matches = re.findall(arxiv_pattern, description)
    
    pdf_urls = []
    seen_papers = set()
    
    for paper_id in matches:
        if paper_id not in seen_papers:
            pdf_urls.append(f"https://arxiv.org/pdf/{paper_id}.pdf")
            seen_papers.add(paper_id)
    
    return pdf_urls

def get_latest_event(events):
    if not events:
        return None
    
    latest_event = None
    latest_date = None
    
    for event in events:
        if 'start_date' not in event:
            continue
            
        try:
            date_str = event['start_date']
            if 'T' in date_str:
                date_str = date_str.split('T')[0] + 'T' + date_str.split('T')[1].rstrip('Z')
                if not date_str.endswith('Z'):
                    date_str += 'Z'
                event_date = datetime.strptime(date_str, '%Y%m%dT%H%M%SZ')
            else:
                event_date = datetime.strptime(date_str, '%Y%m%d')
            
            if latest_date is None or event_date > latest_date:
                latest_date = event_date
                latest_event = event
                
        except ValueError as e:
            print(f"Date parsing error for event {event.get('title', 'Unknown')}: {e}")
            continue
    
    return latest_event

def fetch_pdf():
    print("Fetching calendar data...")
    ics_content = fetch_calendar_data()
    if not ics_content:
        print("Failed to fetch calendar data")
        return None

    print("Parsing calendar events...")
    events = parse_calendar_events(ics_content)
    print(f"Found {len(events)} total events")

    latest_event = get_latest_event(events)
    if not latest_event:
        print("No events found with valid dates")
        return None

    if 'description' not in latest_event:
        print("No description in latest event")
        return None

    arxiv_urls = extract_arxiv_urls(latest_event['description'])
    if not arxiv_urls:
        print("No arXiv papers found in latest event")
        return None

    print(f"Found {len(arxiv_urls)} arXiv papers in latest event: {latest_event.get('title', 'Unknown')}")
    first_url = arxiv_urls[0]
    print(f"Fetching first paper: {first_url}")

    return fetch_pdf_content(first_url)

def fetch_pdf_content(url):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.content

    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

if __name__ == "__main__":
    print("Testing fetch_pdf function...")
    pdf_content = fetch_pdf()
    if pdf_content:
        print(f"Successfully fetched PDF content: {len(pdf_content)} bytes")
    else:
        print("Failed to fetch PDF content")


import io
import PyPDF2
import requests

def extract_text(pdf_content):
    try:
        pdf_file = io.BytesIO(pdf_content)
        reader = PyPDF2.PdfReader(pdf_file)
        full_text = ""
        for page in reader.pages:
            full_text += page.extract_text() + "\n"
        return full_text.replace("\n\n", "\n").strip()
    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def prepare_podcast_text_gemini(text, api_key):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={api_key}"
    prompt = f"""
    You are the narrator of a technical research podcast. 
    Generate a podcast-style script that dives directly into the content without preamble.
    Maintain a confident, authoritative tone while weaving in precise technical terminology. 
    Summarize the research in an engaging flow, highlighting methodology, data-driven insights, 
    experimental design, and theoretical implications. Avoid oversimplifying; assume the audience 
    is familiar with advanced concepts in the domain.
    Do mention all key aspects and key details in the paper.
    Goal is to make this summary as informative and comprehensive as possible.
    The script should sound like a professional research briefing intended for expert listeners.

    Research paper content:
    {text[:20000000]}
    """
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        try:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            print("Gemini API returned unexpected format")
            return None
    else:
        print(f"Gemini API error: {response.status_code}")
        return None

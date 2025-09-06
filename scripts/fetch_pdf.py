import requests

def fetch_pdf(url):
    print("Downloading PDF")
    try:
        response = requests.get(url)
        response.raise_for_status()
        print("Pdf downloaded successfully")
        return response.content
    except Exception as e:
        print(f"Error downloading pdf: {e}")
        return None

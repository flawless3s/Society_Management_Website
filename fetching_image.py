import requests

def fetch_image_from_google_drive(google_drive_url):
    if not google_drive_url:  # Check if the URL is None or an empty string
        return None

    try:
        response = requests.get(google_drive_url, timeout=30)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.content
    except requests.exceptions.Timeout:
        print("Request timed out. Check your connection.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None
    
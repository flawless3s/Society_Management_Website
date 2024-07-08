import requests
def fetch_image_from_google_drive(google_drive_url):
    try:
        response = requests.get(google_drive_url, timeout=30)
        return response.content  # Increase timeout to 10 seconds or more
    # Process the response
    except requests.exceptions.Timeout:
        print("Request timed out. Check your connection.")
    
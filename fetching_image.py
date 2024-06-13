import requests
def fetch_image_from_google_drive(google_drive_url):
    response = requests.get(google_drive_url)
    return response.content
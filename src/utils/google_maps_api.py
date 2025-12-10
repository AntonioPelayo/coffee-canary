import requests

from src.config import GOOGLE_MAPS_API_KEY

GEOCODE_REQUEST_URL_TEMPLATE = "https://maps.googleapis.com/maps/api/geocode/json?address={location}&key={api_key}"

def geocode_location(location: str) -> tuple[float, float]:
    """Get latitude and longitude for a given location using Google Maps Geocoding API."""
    if GOOGLE_MAPS_API_KEY == 'No Key Found' or not location:
        return None, None
    try:
        result = requests.get(
            GEOCODE_REQUEST_URL_TEMPLATE.format(
                location=location.strip().replace(" ", "+"),
                api_key=GOOGLE_MAPS_API_KEY
            )
        )
        latlon = result.json()['results'][0]['geometry']['location']
    except Exception as e:
        print(f"Error geocoding location '{location}': {e}")
        return None, None
    return latlon['lat'], latlon['lng']

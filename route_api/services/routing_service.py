
import requests

class RoutingService:
    BASE_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

    def __init__(self, api_key):
        self.api_key = api_key

    def get_route(self, start_coords, end_coords):
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

        body = {
            "coordinates": [start_coords, end_coords]
        }

        response = requests.post(self.BASE_URL, json=body, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()

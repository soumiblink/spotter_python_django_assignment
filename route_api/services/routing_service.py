import requests


class RoutingService:
    BASE_URL = "https://api.openrouteservice.org/v2/directions/driving-car"

    def __init__(self, api_key):
        self.api_key = api_key

    def get_route(self, start, end):
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

        body = {
            "coordinates": [
                start,   # already list
                end      # already list
            ]
        }

        response = requests.post(self.BASE_URL, json=body, headers=headers)

        return response.json()

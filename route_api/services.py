import requests
import csv


class RoutingService:
    """Service to handle routing via OpenRouteService API"""
    
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openrouteservice.org/v2/directions/driving-car"
    
    def get_route(self, start_coords, end_coords):
        """
        start_coords: [longitude, latitude]
        end_coords: [longitude, latitude]
        """
        try:
            headers = {
                "Authorization": self.api_key,
                "Content-Type": "application/json"
            }

            # Already list → just use directly
            params = {
                "coordinates": [
                    start_coords,
                    end_coords
                ]
            }

            url = "https://api.openrouteservice.org/v2/directions/driving-car"

            response = requests.post(url, json=params, headers=headers)
            return response.json()

        except Exception as e:
            return {"error": str(e)}



class FuelOptimizer:
    """Service to optimize fuel stops along a route"""
    
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.fuel_data = self._load_fuel_data()
    
    def _load_fuel_data(self):
        """Load fuel prices from CSV"""
        try:
            data = []
            with open(self.csv_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    data.append(row)
            return data
        except Exception as e:
            print(f"Error loading fuel data: {e}")
            return []
    
    def find_stops(self, coordinates, distance_miles, mpg=25.0):
        """
        Find optimal fuel stops along route
        Assumes 25 MPG and 15-gallon tank by default
        Returns: (stops, total_cost, total_gallons)
        """
        gallons_needed = distance_miles / mpg
        
        # Placeholder stops
        stops = [
            {"location": "Stop 1", "lat": coordinates[0][1], "lng": coordinates[0][0]},
            {"location": "Stop 2", "lat": coordinates[-1][1], "lng": coordinates[-1][0]}
        ]
        
        total_cost = gallons_needed * 3.50  # Assume $3.50 per gallon
        
        return stops, round(total_cost, 2), round(gallons_needed, 2)
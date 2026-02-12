import requests
import csv
import math


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
        data = []
        try:
            with open(self.csv_path, "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    try:
                        row["retail_price"] = float(row["retail_price"])
                        row["latitude"] = float(row["latitude"])
                        row["longitude"] = float(row["longitude"])
                        data.append(row)
                    except:
                        continue
        except Exception as e:
            print(f"Error loading fuel data: {e}")

        return data

    def _get_cheapest_station(self):
        """Return cheapest fuel station"""
        if not self.fuel_data:
            return None

        return min(self.fuel_data, key=lambda x: x["retail_price"])

    def find_stops(self, route_coordinates, distance_miles, mpg=25.0, tank_size=15.0):
        """
        Find fuel stops based on tank capacity
        """

        max_range = mpg * tank_size  # e.g. 25 * 15 = 375 miles
        gallons_needed = distance_miles / mpg

        # Number of refuels required
        refuels = max(0, math.ceil(distance_miles / max_range) - 1)

        stops = []
        cheapest_station = self._get_cheapest_station()

        total_cost = 0

        if cheapest_station:
            price = cheapest_station["retail_price"]
        else:
            price = 3.50  # fallback price

        remaining_distance = distance_miles

        for i in range(refuels):
            fuel_needed = min(tank_size, remaining_distance / mpg)
            cost = fuel_needed * price
            total_cost += cost

            stops.append({
                "station": cheapest_station["truckstop_name"] if cheapest_station else "Generic Station",
                "lat": cheapest_station["latitude"] if cheapest_station else route_coordinates[0][0],
                "lng": cheapest_station["longitude"] if cheapest_station else route_coordinates[0][1],
                "gallons_filled": round(fuel_needed, 2),
                "price_per_gallon": price,
                "cost": round(cost, 2)
            })

            remaining_distance -= max_range

        # Final cost for total trip
        total_cost = gallons_needed * price

        return stops, round(total_cost, 2), round(gallons_needed, 2)
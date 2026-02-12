import csv
import math
import requests


# =====================================================
# ROUTING SERVICE
# =====================================================

class RoutingService:
    """
    Handles OpenRouteService API communication.
    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openrouteservice.org/v2/directions/driving-car"

    def get_route(self, start_coords, end_coords):
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }

        body = {
            "coordinates": [
                start_coords,
                end_coords,
            ]
        }

        response = requests.post(
            self.base_url,
            json=body,
            headers=headers,
            timeout=15,
        )

        response.raise_for_status()
        return response.json()


# =====================================================
# FUEL OPTIMIZER
# =====================================================

class FuelOptimizer:
    """
    Advanced fuel optimization service.
    Determines dynamic stop points and selects cheapest nearby stations.
    """

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.fuel_data = self._load_fuel_data()

    # ----------------------------------------
    # Load Fuel Data
    # ----------------------------------------

    def _load_fuel_data(self):
        data = []

        try:
            with open(self.csv_path, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    try:
                        data.append({
                            "name": row["truckstop_name"],
                            "retail_price": float(row["retail_price"]),
                            "latitude": float(row["latitude"]),
                            "longitude": float(row["longitude"]),
                        })
                    except (KeyError, ValueError):
                        continue
        except Exception as e:
            print(f"Fuel CSV load error: {e}")

        return data

    # ----------------------------------------
    # Haversine Distance (miles)
    # ----------------------------------------

    def _haversine(self, lat1, lon1, lat2, lon2):
        R = 3958.8

        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)

        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    # ----------------------------------------
    # Find coordinate at X miles along route
    # ----------------------------------------

    def _coordinate_at_distance(self, route_coordinates, target_miles):
        accumulated = 0

        for i in range(1, len(route_coordinates)):
            lon1, lat1 = route_coordinates[i - 1]
            lon2, lat2 = route_coordinates[i]

            segment = self._haversine(lat1, lon1, lat2, lon2)
            accumulated += segment

            if accumulated >= target_miles:
                return lon2, lat2

        return route_coordinates[-1]

    # ----------------------------------------
    # Nearby stations
    # ----------------------------------------

    def _nearby_stations(self, lon, lat, buffer_miles=10):
        stations = []

        for station in self.fuel_data:
            distance = self._haversine(
                lat,
                lon,
                station["latitude"],
                station["longitude"],
            )

            if distance <= buffer_miles:
                stations.append(station)

        return stations

    # ----------------------------------------
    # Main Optimization
    # ----------------------------------------

    def find_stops(
        self,
        route_coordinates,
        distance_miles,
        mpg=25.0,
        tank_size=15.0,
        buffer_distance=10,
    ):

        max_range = mpg * tank_size
        gallons_needed_total = distance_miles / mpg

        refuels = max(0, math.ceil(distance_miles / max_range) - 1)

        stops = []
        total_cost = 0
        remaining_distance = distance_miles

        for stop_index in range(1, refuels + 1):

            target_distance = stop_index * max_range

            stop_lon, stop_lat = self._coordinate_at_distance(
                route_coordinates,
                target_distance,
            )

            nearby = self._nearby_stations(
                stop_lon,
                stop_lat,
                buffer_distance,
            )

            if nearby:
                chosen = min(nearby, key=lambda x: x["retail_price"])
            else:
                chosen = {
                    "name": "Generic Station",
                    "retail_price": 3.50,
                    "latitude": stop_lat,
                    "longitude": stop_lon,
                }

            fuel_needed = min(tank_size, remaining_distance / mpg)
            cost = fuel_needed * chosen["retail_price"]

            total_cost += cost
            remaining_distance -= max_range

            stops.append({
                "station": chosen["name"],
                "lat": chosen["latitude"],
                "lng": chosen["longitude"],
                "gallons_filled": round(fuel_needed, 2),
                "price_per_gallon": round(chosen["retail_price"], 2),
                "cost": round(cost, 2),
            })

        return (
            stops,
            round(total_cost, 2),
            round(gallons_needed_total, 2),
        )

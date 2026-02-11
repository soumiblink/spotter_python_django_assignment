
import pandas as pd
from geopy.distance import geodesic

MAX_RANGE = 500
MPG = 10

class FuelOptimizer:

    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)

    def find_stops(self, route_coords, total_distance_miles):
        stops = []
        total_cost = 0
        remaining_range = MAX_RANGE
        gallons_full = MAX_RANGE / MPG

        for lon, lat in route_coords[::50]:
            nearby = self.df.copy()
            nearby["distance"] = nearby.apply(
                lambda row: geodesic((lat, lon), (row["latitude"], row["longitude"])).miles,
                axis=1
            )
            nearby = nearby.sort_values("price")

            if remaining_range <= 50:
                cheapest = nearby.iloc[0]
                cost = gallons_full * cheapest["price"]
                total_cost += cost
                stops.append({
                    "station": cheapest["station_name"],
                    "price": cheapest["price"],
                    "location": [cheapest["latitude"], cheapest["longitude"]]
                })
                remaining_range = MAX_RANGE

            remaining_range -= 50

        total_gallons = total_distance_miles / MPG
        return stops, round(total_cost, 2), round(total_gallons, 2)

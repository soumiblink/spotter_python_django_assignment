import os
import hashlib
import polyline

from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import RoutingService, FuelOptimizer


class RouteOptimizationView(APIView):

    def post(self, request):
        try:
            start = request.data.get("start_coords")
            end = request.data.get("end_coords")

            if not start or not end:
                return Response(
                    {"error": "Provide start_coords and end_coords"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Safe cache key
            cache_key = hashlib.md5(f"{start}_{end}".encode()).hexdigest()
            cached = cache.get(cache_key)
            if cached:
                return Response(cached)

            api_key = os.getenv("ORS_API_KEY")
            if not api_key:
                return Response(
                    {"error": "ORS_API_KEY not set"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            routing = RoutingService(api_key)
            route_data = routing.get_route(start, end)

            # ✅ Check correct ORS response format
            if not route_data or "routes" not in route_data:
                return Response(
                    {
                        "error": "Routing API failed",
                        "routing_response": route_data
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            route = route_data["routes"][0]

            distance_meters = route["summary"]["distance"]
            distance_miles = distance_meters * 0.000621371

            # ✅ Decode polyline geometry
            encoded_geometry = route["geometry"]
            decoded_coordinates = polyline.decode(encoded_geometry)

            # polyline gives (lat, lon)
            # Convert to (lon, lat) to match your FuelOptimizer
            coordinates = [(lon, lat) for lat, lon in decoded_coordinates]

            optimizer = FuelOptimizer("data/fuel-prices-for-be-assessment.csv")
            stops, total_cost, gallons = optimizer.find_stops(
                coordinates,
                distance_miles
            )

            response_data = {
                "total_distance_miles": round(distance_miles, 2),
                "fuel_stops": stops,
                "total_fuel_cost": total_cost,
                "total_gallons_used": gallons,
                "route_geometry": encoded_geometry
            }

            cache.set(cache_key, response_data, timeout=3600)

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            print(f"Error: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

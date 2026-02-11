
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .services.routing_service import RoutingService
from .services.fuel_optimizer import FuelOptimizer
import os

class RouteOptimizationView(APIView):

    def post(self, request):
        start = request.data.get("start_coords")
        end = request.data.get("end_coords")

        if not start or not end:
            return Response({"error": "Provide start_coords and end_coords"}, status=400)

        cache_key = f"{start}_{end}"
        cached = cache.get(cache_key)
        if cached:
            return Response(cached)

        api_key = os.getenv("ORS_API_KEY")
        if not api_key:
            return Response({"error": "ORS_API_KEY not set"}, status=500)

        routing = RoutingService(api_key)
        route_data = routing.get_route(start, end)

        distance_meters = route_data["features"][0]["properties"]["summary"]["distance"]
        distance_miles = distance_meters * 0.000621371

        coordinates = route_data["features"][0]["geometry"]["coordinates"]

        optimizer = FuelOptimizer("data/fuel-prices-for-be-assessment.csv")
        stops, total_cost, gallons = optimizer.find_stops(coordinates, distance_miles)

        response_data = {
            "total_distance_miles": round(distance_miles, 2),
            "fuel_stops": stops,
            "total_fuel_cost": total_cost,
            "total_gallons_used": gallons,
            "route_geometry": route_data["features"][0]["geometry"]
        }

        cache.set(cache_key, response_data)

        return Response(response_data, status=status.HTTP_200_OK)

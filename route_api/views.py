import os
import hashlib
import logging
from urllib import request
import polyline
import logging

logger = logging.getLogger(__name__)


from django.conf import settings
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import RoutingService, FuelOptimizer
from .serializers import RouteOptimizationSerializer



logger = logging.getLogger(__name__)


class RouteOptimizationView(APIView):
    """
    API endpoint to:
    - Fetch route from ORS
    - Decode geometry
    - Calculate optimized fuel stops
    - Return total fuel cost and trip details
    """

    def post(self, request):
        try:
            # ------------------------------
            # Serializer Validation
            # ------------------------------
            serializer = RouteOptimizationSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            validated_data = serializer.validated_data

            start = validated_data["start_coords"]
            end = validated_data["end_coords"]
            mpg = validated_data["mpg"]
            tank_size = validated_data["tank_size"]

            # ------------------------------
            # Caching
            # ------------------------------
            cache_key_raw = f"{start}_{end}_{mpg}_{tank_size}"
            cache_key = hashlib.md5(cache_key_raw.encode()).hexdigest()

            cached_response = cache.get(cache_key)
            if cached_response:
                return Response(cached_response)

            # ------------------------------
            # ORS API Key Check
            # ------------------------------
            api_key = os.getenv("ORS_API_KEY")
            if not api_key:
                return Response(
                    {"error": "ORS_API_KEY not set"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            routing_service = RoutingService(api_key)
            route_data = routing_service.get_route(start, end)

            if not route_data or "routes" not in route_data:
                return Response(
                    {
                        "error": "Routing API failed",
                        "routing_response": route_data,
                    },
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )

            route = route_data["routes"][0]

            # ------------------------------
            # Distance Calculation
            # ------------------------------
            distance_meters = route["summary"]["distance"]
            distance_miles = distance_meters * 0.000621371

            # ------------------------------
            # Decode Polyline
            # ------------------------------
            encoded_geometry = route["geometry"]
            decoded_coordinates = polyline.decode(encoded_geometry)

            # polyline returns (lat, lon)
            # convert to (lon, lat)
            route_coordinates = [
                (lon, lat) for lat, lon in decoded_coordinates
            ]

            # ------------------------------
            # Fuel Optimization
            # ------------------------------
            csv_path = os.path.join(
                settings.BASE_DIR,
                "data",
                "fuel-prices-for-be-assessment.csv",
            )

            optimizer = FuelOptimizer(csv_path)

            stops, total_cost, gallons_used = optimizer.find_stops(
                route_coordinates=route_coordinates,
                distance_miles=distance_miles,
                mpg=mpg,
                tank_size=tank_size,
            )

            response_data = {
                "total_distance_miles": round(distance_miles, 2),
                "total_gallons_used": gallons_used,
                "total_fuel_cost": total_cost,
                "fuel_stops": stops,
                "route_geometry": encoded_geometry,
            }

            cache.set(cache_key, response_data, timeout=3600)

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"RouteOptimization Error: {str(e)}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({"status": "Fuel Route Optimizer API running"})

urlpatterns = [
    path("", home),
    path("api/", include("route_api.urls")),
]

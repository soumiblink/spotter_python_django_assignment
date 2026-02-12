from rest_framework import serializers


class RouteOptimizationSerializer(serializers.Serializer):
    start_coords = serializers.ListField(
        child=serializers.FloatField(),
        min_length=2,
        max_length=2,
        required=True
    )
    end_coords = serializers.ListField(
        child=serializers.FloatField(),
        min_length=2,
        max_length=2,
        required=True
    )
    mpg = serializers.FloatField(required=False, default=10.0)
    tank_size = serializers.FloatField(required=False, default=50.0)

    def validate_mpg(self, value):
        if value <= 0:
            raise serializers.ValidationError("MPG must be greater than 0.")
        return value

    def validate_tank_size(self, value):
        if value <= 0:
            raise serializers.ValidationError("Tank size must be greater than 0.")
        return value

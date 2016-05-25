from rest_framework import serializers

from example.app.models import Point


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point

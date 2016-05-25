from rest_framework import serializers

from demo.models import Point


class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point

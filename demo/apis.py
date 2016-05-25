from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from demo.models import Point
from demo.serializers import PointSerializer


class TestViewSet(GenericViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer

    def list(self, request, *args, **kwargs):
        data = Point.objects.filter(position__geostarts='wtmtkx')
        return Response(PointSerializer(data, many=True).data)

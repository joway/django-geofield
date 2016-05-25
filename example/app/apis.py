from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from example.app.models import Point
from example.app.serializers import PointSerializer


class TestViewSet(GenericViewSet):
    queryset = Point.objects.all()
    serializer_class = PointSerializer

    def list(self, request, *args, **kwargs):
        data = Point.objects.filter(position__geosearch='wtmtkx')
        return Response(PointSerializer(data, many=True).data)

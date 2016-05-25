import random
from os import environ
from unittest import TestCase

import numpy
from haversine import haversine

from example.app.models import Point
from geofield import GeoPosition
from geofield.geohash import geo_decode_exactly, geo_encode, geo_expand


class TestGeoHash(TestCase):
    def setUp(self):
        environ.setdefault("DJANGO_SETTINGS_MODULE", "geofield.tests.settings")
        self.precision = 6
        for lat in numpy.arange(30.0, 30.00001, 0.0000001):
            for lon in numpy.arange(120, 120.00001, 0.0000001):
                Point.objects.create(
                    position=GeoPosition(lat + random.random(), lon + random.random(), precision=self.precision))

    def test_get_all(self):
        print("Total object count is : " + str(Point.objects.all().count()))

    def test_start_with(self):
        pos = Point.objects.get(id=100)
        points_matched = Point.objects.filter(position__startswith=pos.position.geohash)

        self.handler_data(pos, points_matched, 2)

    def test_search(self):
        pos = Point.objects.get(id=100)

        points_matched = Point.objects.filter(position__geosearch=pos.position.geohash)

        self.handler_data(pos, points_matched, 4)

    def test_geoprecise(self):
        pos = Point.objects.get(id=100)
        print(pos)
        points_matched = Point.objects.filter(position__geoprecise=pos.position.geohash)

        self.handler_data(pos, points_matched, 2)

    def handler_data(self, pos, points_matched, count=2):
        lat_width, lon_height = geo_decode_exactly(pos.position.get_geohash())[2:4]
        print('default error is : ', lat_width, lon_height)

        for i in points_matched:
            self.assertTrue(geo_encode(i.position.get_latitude(),
                                       i.position.get_longitude(), precision=self.precision) in
                            geo_expand(i.position.get_geohash()))

            print('error is :', abs(pos.position.get_latitude() - i.position.get_latitude()))
            print('error is :', abs(pos.position.get_longitude() - i.position.get_longitude()))

            self.assertTrue(abs(pos.position.get_latitude() - i.position.get_latitude()) < lat_width * count)
            self.assertTrue(
                abs(pos.position.get_longitude() - i.position.get_longitude()) < lon_height * count)
            print('distance is : ', haversine((pos.position.get_latitude(),
                                               pos.position.get_longitude()),
                                              (i.position.get_latitude(),
                                               i.position.get_longitude())))

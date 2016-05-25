# Create your tests here.
import random

import numpy
from django.test import TestCase

from demo.models import Point
from django_geohash import GeoPosition
from django_geohash.geohash import geo_expand, geo_decode_exactly


class DemoTestCase(TestCase):
    def setUp(self):
        for lat in numpy.arange(30.0, 30.01, 0.0001):
            for lon in numpy.arange(120, 120.01, 0.0001):
                Point.objects.create(position=GeoPosition(lat + random.random(), lon + random.random(), precision=6))

    def test_search(self):
        for i in range(0, 2):
            pos = Point.objects.all()
            print(pos)
            pos = pos[0]
            geohash_matched = geo_expand(pos.geohash)
            geohash_matched.append(pos.geohash)

            # 计算误差:
            print("------- width and height: ------")
            lat_width, lon_height = geo_decode_exactly(pos.geohash)[2:4]
            print('允许误差', lat_width, lon_height)

            print("------- 目标点: ------\n" + str(pos))
            print("------- 搜索结果: ------")
            positions = Point.objects.filter(position__search=pos.geohash)
            print(positions)
            # for i in self.positions:
            #     if i.geohash_code in geohash_matched:
            #         # 只保留在搜索范围框内的点
            #         if abs(i.lat - pos.lat) < lat_width \
            #                 and abs(i.lon - pos.lon) < lon_height:
            #             print(i)
            #             print('lat 误差: ', abs(i.lat - pos.lat))
            #             print('距离: ', haversine((i.lat, i.lon), (pos.lat, pos.lon)))

    def tearDown(self):
        print('结束')

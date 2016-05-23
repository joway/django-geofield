import random
import unittest

import numpy
from haversine import haversine

from geo_position import GeoPosition
from geohash import decode, encode, expand, decode_exactly


class TestGeoHash(unittest.TestCase):
    def setUp(self):
        self.positions = []
        for lat in numpy.arange(30.0, 30.01, 0.00001):
            for lon in numpy.arange(120, 120.001, 0.00001):
                self.positions.append(GeoPosition(lat + random.random(), lon + random.random(), 6))

    # def test_decode_and_encode(self):
    #     for i in self.positions:
    #         lat, lon = decode(i.geohash_code)
    #         self.assertTrue(encode(lat, lon), i.geohash_code)

    def test_search(self):
        pos = self.positions[100]
        geohash_matched = expand(pos.geohash_code)
        geohash_matched.append(pos.geohash_code)

        # 计算误差:
        print("------- width and height: ------")
        lat_width, lon_height = decode_exactly(pos.geohash_code)[2:4]
        print('允许误差', lat_width, lon_height)

        print("------- 目标点: ------\n" + str(pos))
        print("------- 搜索结果: ------")
        for i in self.positions:
            if i.geohash_code in geohash_matched:
                # 只保留在搜索范围框内的点
                if abs(i.lat - pos.lat) < lat_width \
                        and abs(i.lon - pos.lon) < lon_height:
                    print(i)
                    print('lat 误差: ', abs(i.lat - pos.lat))
                    print('距离: ', haversine((i.lat, i.lon), (pos.lat, pos.lon)))

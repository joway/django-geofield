# coding: UTF-8

from __future__ import unicode_literals

from decimal import Decimal

from django_geofield.geohash import geo_encode

VERSION = (0, 0, 2)
__version__ = '.'.join(map(str, VERSION))


class GeoPosition(object):
    def __init__(self, latitude, longitude, geohash_code=None, precision=9):
        if not geohash_code:
            geohash_code = geo_encode(latitude, longitude, precision)

        self.latitude = Decimal(latitude)
        self.longitude = Decimal(longitude)
        self.geohash = geohash_code

    def __str__(self):
        return "%s,%s,%s" % (self.geohash, self.latitude, self.longitude)

    def __repr__(self):
        return "GeoPosition(%s)" % str(self)

    def __len__(self):
        return len(str(self))

    # make it ep when geohash is same
    def __eq__(self, other):
        return isinstance(other, GeoPosition) and self.geohash == other.geohash

    def __ne__(self, other):
        return not isinstance(other, GeoPosition) or self.geohash != other.geohash

    def __gt__(self, other):
        return not isinstance(other, GeoPosition) or self.geohash > other.geohash

    def __lt__(self, other):
        return not isinstance(other, GeoPosition) or self.geohash < other.geohash

    def get_latitude(self):
        return Decimal(self.latitude)

    def get_longitude(self):
        return Decimal(self.longitude)

    def get_geohash(self):
        return self.geohash

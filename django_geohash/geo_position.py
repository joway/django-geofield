from geohash import encode


class GeoPosition(object):
    def __init__(self, lat, lon, precision=12):
        # 纬度
        self.lat = lat
        # 经度
        self.lon = lon

        self.geohash_code = encode(lat, lon, precision)

    def __str__(self):
        return "(%s %s) : %s" % (self.lat, self.lon, self.geohash_code)

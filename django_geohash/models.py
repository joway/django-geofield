from django.db import models

from django_geohash.geohash import geo_encode


class GeoPositionManager(models.Manager):
    def create_geo_position(self, lat, lon, **extra_fields):
        position = self.model(lat=lat,
                              lon=lon,
                              geohash=geo_encode(lat, lon),
                              **extra_fields)
        position.save(using=self._db)
        return position


class GeoPosition(models.Model):
    lat = models.DecimalField('latitude', unique=True, max_digits=2 + 32, decimal_places=32)
    lon = models.DecimalField('longitude', unique=True, max_digits=3 + 32, decimal_places=32)

    geohash = models.CharField('geohash', max_length=32)

    objects = GeoPositionManager()

    def __str__(self):
        return "(%s %s) : %s" % (self.lat, self.lon, self.geohash_code)

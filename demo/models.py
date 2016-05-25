from django.db import models

# Create your models here.
from django_geohash.fields import GeoPositionField


class Point(models.Model):
    address = models.CharField(max_length=32,default='None')
    position = GeoPositionField(db_index=True)

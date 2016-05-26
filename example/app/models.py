from django.db import models

# Create your models here.

from django_geofield.fields import GeoPositionField


class Point(models.Model):
    position = GeoPositionField(db_index=True)

    def __str__(self):
        return str(self.position)

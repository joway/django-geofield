=====
Django-GeoField
=====

A lightweight Django Geo Field to save and handle Geo Points. It supports to search the nearby points by their geohash.

Quick start
-----------

0. Install django-geofield

pip install django-geofield

1. Add "django-geofield" to your INSTALLED_APPS setting like this::

        INSTALLED_APPS = (
            ...
            'django-geofield',
        )

2. Define GeoPositionField in your Model like this::

        class Point(models.Model):
            ...
            position = GeoPositionField(db_index=True)

3. Run `python manage.py makemigrations` and `python manage.py migrate` to make it effect

4. The field will save a geo point with a string into database like this :

        Point.objects.create(
                        position=GeoPosition(lat, lon, precision=6))

        'wtmm7w,30.49145747305400533377905958332121372222900390625,120.042387425481223317547119222581386566162109375'

5. If you want to query the points whose geohash is matched exactly with the given point , you can :

        pos = Point.objects.get(id=1)

        points_matched = Point.objects.filter(position__geoprecise=pos.position.geohash)


    The '__geoprecise' will find all points have the same geohash.

6. If you want to query the points in expand area to eliminate the geohash's marginal error, you can :

        pos = Point.objects.get(id=1)

        points_matched = Point.objects.filter(position__geosearch=pos.position.geohash)

    The '__geosearch' lookup will find all points have one of 9 ( 1 center point and 8 expand point) geohash .



### **License**: MIT


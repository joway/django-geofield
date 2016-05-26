Django-GeoField
=====
![](https://api.travis-ci.org/joway/django-geofield.svg?branch=master)

A lightweight Django Geo Field to save and handle Geo Points. It supports to search the nearby points by their geohash.

Quick start
-----------

0. Install django-geofield

        pip install django-geofield

1. Define GeoPositionField in your Model like this::

        class Point(models.Model):
            ...
            position = GeoPositionField(db_index=True)

2. Run `python manage.py makemigrations` and `python manage.py migrate` to make it effect

3. The field will save a geo point with a string into database like this :

        Point.objects.create(
                        position=GeoPosition(lat, lon, precision=6))

        'wtmm7w,30.49145747305400533377905958332121372222900390625,120.042387425481223317547119222581386566162109375'

4. If you want to query the points whose geohash is matched exactly with the given point , you can :

        pos = Point.objects.get(id=1)

        points_matched = Point.objects.filter(position__geoprecise=pos.position.geohash)


    The '__geoprecise' lookup will find all points have the same geohash.

5. If you want to query the points in expand area to eliminate the geohash's marginal error, you can :

        pos = Point.objects.get(id=1)

        points_matched = Point.objects.filter(position__geosearch=pos.position.geohash)

    The '__geosearch' lookup will find all points have one of 9 ( 1 center point and 8 expand point) geohash .


6. If you want to query the points within a specific range , you should lookup the geohash table to get the geohash length you want, then just search the cropped length.

        pos = Point.objects.get(id=1)

        points_matched = Point.objects.filter(position__geosearch=pos.position.geohash[0:4])

    ![](http://images.cnitblog.com/blog/522490/201309/09185913-9f6f65fc3d3c40ecb3328970831c625c.png)

#### PS: 

If you want to limit the distance strictly, you should writer your own codes to filter the result .

About GeoHash
------

[Wikipedia](http://en.wikipedia.org/wiki/Geohash)




Support
------

python:
  - "2.7"
  - "3.2"
  - "3.3"
  - "3.4"
  - "3.5"
  - "3.5-dev" # 3.5 development branch
  - "nightly" # currently points to 3.6-dev


Thanks
------

[python-geohash](https://github.com/hkwi/python-geohash/blob/master/geohash.py)

License
------

MIT


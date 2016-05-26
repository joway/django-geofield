# coding: UTF-8

from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Lookup
from django.db.models.lookups import PatternLookup
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _

from . import GeoPosition
from .geohash import geo_expand


def parse_geo_position(geo_position_string):
    """Takes a string of cards and splits into a full hand."""
    # start with geohash
    value_parts = geo_position_string.rsplit(',')
    try:
        geohash = value_parts[0]
        latitude = value_parts[1]
        longitude = value_parts[2]
    except IndexError:
        raise ValidationError("Invalid data format for a GeoPosition instance")

    return GeoPosition(latitude, longitude, geohash)


class GeoPositionField(models.Field):
    description = _("A GeoPosition (latitude and longitude)")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 32
        super(GeoPositionField, self).__init__(*args, **kwargs)

    # Sometimes, though, your database storage is similar in type to some other field,
    # so you can use that other field’s logic to create the right column.
    def get_internal_type(self):
        return 'CharField'

    # Converting values to Python objects,
    # 转化数据库中的字符到 Python的变量
    # from_db_value() is called when the data is loaded from the database
    def from_db_value(self, value, expression, connection, context):
        if value is None:
            return value
        return parse_geo_position(value)

    # to deserialization
    # 把数据库或者序列器返回的值转换成一个python对象
    # to_python() is called by deserialization and during the clean() method used from forms
    # 反序列化
    def to_python(self, value):
        if value is None:
            return value

        if isinstance(value, GeoPosition):
            return value

        if isinstance(value, list) or isinstance(value, tuple):
            return GeoPosition(value[1], value[2], value[0])

        # default case is string
        return parse_geo_position(value)

    # 将Python变量处理后(此处为压缩）保存到数据库
    def get_prep_value(self, value):
        return str(value)

    # 序列化
    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return smart_text(value)


@GeoPositionField.register_lookup
class GeoSearchMatchedLookup(Lookup):
    lookup_name = 'geosearch'

    def __init__(self, lhs, rhs):
        super(GeoSearchMatchedLookup, self).__init__(lhs, rhs)

    def process_rhs(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = super(GeoSearchMatchedLookup, self).process_rhs(compiler, connection)
        rhs = ''
        params = rhs_params[0]
        if params and not self.bilateral_transforms:
            rhs_params = geo_expand(params)
            for i in range(0, len(rhs_params)):

                # start with %s
                rhs_params[i] = "%s%%" % connection.ops.prep_for_like_query(rhs_params[i])

                # sql prepare
                if i < len(rhs_params) - 1:
                    rhs += lhs + ' like %s OR '
                else:
                    rhs += lhs + 'like %s'
        return rhs, rhs_params

    def as_sql(self, compiler, connection):
        # Lookup作用于两个值，lhs和rhs，分别是左边(表名)和右边(字段名)。
        # 左边的值一般是个字段的引用，但是它可以是任何实现了查询表达式API的对象。
        # 右边的值由用户提供。
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        return rhs, params


@GeoPositionField.register_lookup
class GeoPreciseSearchMatchedLookup(PatternLookup):
    lookup_name = 'geoprecise'

    def __init__(self, lhs, rhs):
        super(GeoPreciseSearchMatchedLookup, self).__init__(lhs, rhs)

    def get_rhs_op(self, connection, rhs):
        return connection.operators['startswith'] % rhs

    def process_rhs(self, qn, connection):
        rhs, params = super(GeoPreciseSearchMatchedLookup, self).process_rhs(qn, connection)
        if params and not self.bilateral_transforms:
            params[0] = "%s%%" % connection.ops.prep_for_like_query(params[0])
        return rhs, params

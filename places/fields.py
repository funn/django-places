import decimal
import json

from django.contrib.postgres.fields import JSONField
from django.utils.translation import ugettext_lazy as _

from .forms import PlacesField as PlacesFormField


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)
    #end def
#end class


def decimal_parser(s):
    return decimal.Decimal(str(s))
#end def


class PlacesField(JSONField):
    description = _("A Google Places JSON field (id, name, address, latitude and longitude)")

    def __init__(self, verbose_name=None, name=None, encoder=DecimalEncoder, **kwargs):
        return super(PlacesField, self).__init__(verbose_name, name, encoder, **kwargs)
    #end if

    def to_python(self, value):
        if isinstance(value, str):
            return json.loads(value, parse_float=decimal_parser)
        return value
    #end def

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)
    #end def

    def formfield(self, **kwargs):
        defaults = {'form_class': PlacesFormField}
        defaults.update(kwargs)
        return super(PlacesField, self).formfield(**defaults)
    #end def
#end class

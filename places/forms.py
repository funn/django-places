from django import forms
from django.utils.translation import ugettext_lazy as _

from .widgets import PlacesWidget


class PlacesField(forms.MultiValueField):
    default_error_messages = {'invalid': _('Enter a valid geoposition.')}

    def __init__(self, *args, **kwargs):
        fields = (
            forms.CharField(label=_('place_id')),
            forms.CharField(label=_('name')),
            forms.CharField(label=_('place')),
            forms.DecimalField(label=_('Latitude')),
            forms.DecimalField(label=_('Longitude')),
        )
        self.widget = PlacesWidget()
        super(PlacesField, self).__init__(fields, **kwargs)

    def widget_attrs(self, widget):
        classes = widget.attrs.get('class', '').split()
        classes.append('places')
        return {'class': ' '.join(classes)}

    def compress(self, value_list):
        if value_list:
            return dict(place_id=value_list[0], name=value_list[1], place=value_list[2], latitude=value_list[3], longitude=value_list[4])
        return dict()

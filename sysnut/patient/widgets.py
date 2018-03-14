from dal.widgets import QuerySetSelectMixin
from dal_select2.widgets import Select2, Select2Multiple



class Select2BootstrapWidgetMixin(object):

    def build_attrs(self, *args, **kwargs):
        attrs = super(Select2BootstrapWidgetMixin, self).build_attrs(*args, **kwargs)
        attrs.setdefault('data-theme','bootstrap')
        return attrs

    class Media:
        css = {
            'all': (
                'autocomplete_light/vendor/select2/dist/css/select2.css', # The one from dal_select2.widgets.Select2WidgetMixin
                'css/select2-bootstrap.min.css'  # Bootstrap theme itself
            )
        }

        js = ('autocomplete_light/jquery.init.js',
              'autocomplete_light/autocomplete.init.js',
              'autocomplete_light/vendor/select2/dist/js/select2.full.js',
            'autocomplete_light/select2.js',
        )





class ModelSelect2Bootstrap(QuerySetSelectMixin,
                            Select2BootstrapWidgetMixin,
                            Select2):
    """
    Use this instead of ModelSelect2 widget
    """
    autocomplete_function = 'select2'


class ModelSelect2MultipleBootstrap(QuerySetSelectMixin,
                                    Select2BootstrapWidgetMixin,
                                    Select2Multiple):
    """
    Use this instead of ModelSelect2Multiple widget
    """
    autocomplete_function = 'select2'
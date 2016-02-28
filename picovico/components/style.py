from .base import PicovicoBaseComponent


class PicovicoStyle(PicovicoBaseComponent):
    """ Picovico Style Component class. """
    _plural_url_attrs = ('all', 'library')
    # def __init__(self, request_obj):
        # super(PicovicoStyle, self).__init__(request_obj, 'style')
    def get_url_attr(self, key=None):
        urls = {
            'free': 'PICOVICO_STYLES'
        }
        for k in self._plural_url_attrs:
            urls[k] = 'MY_STYLES'
        return urls.get(key, None) if key else urls

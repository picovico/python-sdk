from .base import PicovicoBaseComponent


class PicovicoStyle(PicovicoBaseComponent):
    """ Picovico Style Component class. """
    def __init__(self, request_obj):
        super(PicovicoStyle, self).__init__(request_obj, 'style')

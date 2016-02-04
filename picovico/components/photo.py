from .base import PicovicoBaseComponent


class PicovicoPhoto(PicovicoBaseComponent):
    """ Picovico Photo Component class. """
    def __init__(self, request_obj):
        super(PicovicoPhoto, self).__init__(request_obj, 'photo')

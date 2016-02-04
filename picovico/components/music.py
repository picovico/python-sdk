from .base import PicovicoBaseComponent


class PicovicoMusic(PicovicoBaseComponent):
    """ Picovico Music Component Class """
    def __init__(self, request_obj):
        super(PicovicoMusic, self).__init__(request_obj, 'music')

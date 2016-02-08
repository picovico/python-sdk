from .base import PicovicoBaseComponent


class PicovicoMusic(PicovicoBaseComponent):
    """ Picovico Music Component Class """
    def __init__(self, request_obj):
        super(PicovicoMusic, self).__init__(request_obj, 'music')

    def _upload_component_url(self, url, preview):
        return super(PicovicoMusic, self)._upload_component_url(url, preview_url=preview)

from .base import PicovicoBaseComponent


class PicovicoPhoto(PicovicoBaseComponent):
    """ Picovico Photo Component class. """
    def __init__(self, request_obj):
        super(PicovicoPhoto, self).__init__(request_obj, 'photo')

    def _upload_component_url(self, url, thumbnail):
        return super(PicovicoMusic, self)._upload_component_url(url, thumbnail_url=thumbnail)

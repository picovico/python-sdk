from .base import PicovicoBaseComponent


class PicovicoPhoto(PicovicoBaseComponent):
    """ Picovico Photo Component class. """
    def __init__(self, request_obj):
        super(PicovicoPhoto, self).__init__(request_obj, 'photo')

    def upload_url(self, url, thumbnail):
        return super(PicovicoPhoto, self).upload_url(url, thumbnail_url=thumbnail)

from .base import PicovicoBaseComponent


class PicovicoPhoto(PicovicoBaseComponent):
    """ Picovico Photo Component class. """
    @property
    def component(self):
        return 'photo'

    def upload_url(self, url, thumbnail):
        return super(PicovicoPhoto, self).upload_url(url, thumbnail_url=thumbnail)

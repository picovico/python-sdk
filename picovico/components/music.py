from .base import PicovicoBaseComponent


class PicovicoMusic(PicovicoBaseComponent):
    """ Picovico Music Component Class """
    @property
    def component(self):
        return 'music'

    def upload_url(self, url, preview):
        return super(PicovicoMusic, self).upload_url(url, preview_url=preview)

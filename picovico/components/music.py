from picovico.components.base import PicovicoBaseComponent


class PicovicoMusic(PicovicoBaseComponent):
    """ Picovico-SDK: Music  component class.
    """

    @property
    def component(self):
        return 'music'

    def upload_url(self, url, preview):
        """ upload music url and music preview

        Args:
            url(str): URL  of music.
            preview(str):  preview url of music.
        """
        return super(PicovicoMusic, self).upload_url(url, preview_url=preview)

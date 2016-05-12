from picovico.components.base import PicovicoBaseComponent


class PicovicoPhoto(PicovicoBaseComponent):
    """ Picovico-SDK: Photo Component class.
    """

    @property
    def component(self):
        return 'photo'

    def upload_url(self, url, thumbnail):
        """ upload photo url and thubnail.

        Args:
            url(str): Photo URL to upload.
            thumbnail(str): Thumbnail URL to upload.
        """
        return super(PicovicoPhoto, self).upload_url(url, thumbnail_url=thumbnail)

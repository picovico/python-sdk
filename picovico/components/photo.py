from .base import PicovicoBaseComponent


class PicovicoPhoto(PicovicoBaseComponent):
    """ Picovico Photo Component class. """
    # def __init__(self, request_obj):
        # super(PicovicoPhoto, self).__init__(request_obj, 'photo')

    def get_url_attr(self, key=None):
        # single = ('one', 'delete')
        # non_single = ('all', 'library', 'upload_file', 'upload_url')
        # urls = {
            # 'free': 'PICOVICO_MUSICS'
        # }
        urls = {}
        for k in self._single_url_attrs:
            urls[k] = 'MY_SINGLE_PHOTO'
        for k in self._plural_url_attrs:
            urls[k] = 'MY_PHOTOS'
        return urls.get(key, None) if key else urls

    def upload_url(self, url, thumbnail):
        return super(PicovicoPhoto, self).upload_url(url, thumbnail_url=thumbnail)

from .base import PicovicoBaseComponent


class PicovicoMusic(PicovicoBaseComponent):
    """ Picovico Music Component Class """
    _plural_url_attrs = PicovicoBaseComponent._plural_url_attrs + ('library',)
    # def __init__(self, request_obj):
        # super(PicovicoMusic, self).__init__(request_obj, 'music')

    def get_url_attr(self, key=None):
        # single = ('one', 'delete')
        # non_single = ('all', 'library', 'upload_file', 'upload_url')
        urls = {
            'free': 'PICOVICO_MUSICS'
        }
        for k in self._single_url_attrs:
            urls[k] = 'MY_SINGLE_MUSIC'
        for k in self._plural_url_attrs:
            urls[k] = 'MY_MUSICS'
        return urls.get(key, None) if key else urls

    def upload_url(self, url, preview):
        return super(PicovicoMusic, self).upload_url(url, preview_url=preview)

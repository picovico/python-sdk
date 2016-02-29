from .base import PicovicoBaseComponent
from .. import decorators as pv_decorator
from .. import urls as pv_urls
from .. import constants as pv_constants


class PicovicoVideo(PicovicoBaseComponent):
    """ Picovico Video Component class. """
    @property
    def component(self):
        return 'video'

    @pv_decorator.pv_auth_required
    def preview(self, video_id):
        '''
            Picovico: Make a preview request for the project.
            144p video preview is available for the style.
            Rendering state of the video will not be changed.
        '''
        req_args = elf.create_request_args(**{
            'method': 'post',
            'url_attr': 'MY_SINGLE_VIDEO_PREVIEW'.format(video_id),
        })
        return self._api_call(**req_args)

    @pv_decorator.pv_auth_required
    def create(self, video_id):
        '''
            Picovico: Sends the actual rendering request to rendering engine
        '''
        req_args = self.create_request_args(**{
            'method': 'post',
            'url_attr': 'MY_SINGLE_VIDEO_CREATE'.format(video_id),
        })
        return self._api_call(**req_args)

    @pv_decorator.pv_auth_required
    def duplicate(self, video_id):
        '''
            Picovico: Duplicates any video and saves it to the new draft or overrides if any exists.
        '''
        req_args = self.create_request_args(**{
            'method': 'post',
            'url': 'MY_SINGLE_VIDEO_DUPLICATE'.format(video_id),
        })
        return self._api_call(**req_args)

    @pv_decorator.pv_auth_required
    def new(self, name=None):
        req_args = self.create_request_args(**{
            'method': 'post',
            'url_attr': 'MY_VIDEOS',
            'post_data': {'name': name or pv_constants.VIDEO_NAME}
        })
        return self._api_call(**req_args)

    @pv_decorator.pv_auth_required
    def save(self, vdd):
        req_args = self.create_request_args(**{
            'method': 'post',
            'url_attr': 'MY_VIDEOS',
            'post_data': vdd
        })
        return self._api_call(**req_args)
        
        #self.vdd = {
            #'style': self.style
        #}

        #req_args = {
            #'method':
        #}

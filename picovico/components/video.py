from .base import PicovicoBaseComponent
from .. import decorators as pv_decorator
from .. import urls as pv_urls


class PicovicoVideo(PicovicoBaseComponent):
    """ Picovico Video Component class. """
    def __init__(self, request_obj):
        super(PicovicoVideo, self).__init__(request_obj, 'video')

    @pv_decorator.pv_auth_required
    def preview_video(self, video_id):
        '''
            Picovico: Make a preview request for the project. 
            144p video preview is available for the style.
            Rendering state of the video will not be changed.
        '''
        req_args = {
            'method': 'post',
            'url': getattr(pv_urls, 'MY_SINGLE_VIDEO_PREVIEW'.format(video_id)),
        }
        return self._api_call(**req_args)
        
    @pv_decorator.pv_auth_required
    def create_video(self, video_id):
        '''
            Picovico: Sends the actual rendering request to rendering engine
        '''
        req_args = {
            'method': 'post',
            'url': getattr(pv_urls, 'MY_SINGLE_VIDEO_CREATE'.format(video_id)),
        }
        return self._api_call(**req_args)
        
    @pv_decorator.pv_auth_required
    def duplicate_video(self, video_id):
        '''
            Picovico: Duplicates any video and saves it to the new draft or overrides if any exists.
        '''
        req_args = {
            'method': 'post',
            'url': getattr(pv_urls, 'MY_SINGLE_VIDEO_DUPLICATE'.format(video_id)),
        }
        return self._api_call(**req_args)

    @pv_decorator.pv_auth_required
    def begin_project(self, name=None):
        req_args = {
            'method': 'post',
            'url': pv_urls.MY_VIDEOS
            'data': {'name': name or 'Untitled From Picovico Client.'}
        }
        return self._api_call(**req_args)
        

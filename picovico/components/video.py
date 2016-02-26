from .base import PicovicoBaseComponent
from .. import decorators as pv_decorator
from .. import urls as pv_urls


class PicovicoVideo(PicovicoBaseComponent):
    """ Picovico Video Component class. """
    def __init__(self, request_obj):
        super(PicovicoVideo, self).__init__(request_obj, 'video')

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
            'data': {'name': name or 'Untitled From Picovico Client.'}
        })
        return self._api_call(**req_args)
    
    @pv_decorator.pv_auth_required
    def save(self):
        pass
        #self.vdd = {
            #'style': self.style
        #}
        
        #req_args = {
            #'method': 
        #}

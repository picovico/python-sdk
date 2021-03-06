from picovico.components.base import PicovicoBaseComponent
from picovico import decorators as pv_decorators
from picovico import urls as pv_urls
from picovico import constants as pv_constants


class PicovicoVideo(PicovicoBaseComponent):
    """ Picovico-SDK: Picovico Video Component class.
    """

    @property
    def component(self):
        return 'video'

    def _api_call(self, **kwargs):
        id = kwargs.pop('video_id', None)
        if id:
            url_path = kwargs.get('path')
            kwargs.update(path=url_path.format(video_id=id))
        return super(PicovicoVideo, self)._api_call(**kwargs)

    @pv_decorators.pv_auth_required
    def preview(self, video_id):
        '''
            Picovico: Make a preview request for the project.
            144p video preview is available for the style.
            Rendering state of the video will not be changed.
        '''
        req_args = self.create_request_args(**{
            'method': 'post',
            'url_attr': 'MY_SINGLE_VIDEO_PREVIEW',
        })
        return self._api_call(video_id=video_id, **req_args)

    @pv_decorators.pv_auth_required
    def create(self, video_id):
        '''
            Picovico: Sends the actual rendering request to rendering engine
        '''
        req_args = self.create_request_args(**{
            'method': 'post',
            'url_attr': 'MY_SINGLE_VIDEO_CREATE',
        })
        return self._api_call(video_id=video_id, **req_args)

    @pv_decorators.pv_auth_required
    def duplicate(self, video_id):
        '''
            Picovico: Duplicates any video and saves it to the new draft or overrides if any exists.
        '''
        req_args = self.create_request_args(**{
            'method': 'post',
            'url_attr': 'MY_SINGLE_VIDEO_DUPLICATE',
        })
        return self._api_call(video_id=video_id, **req_args)

    @pv_decorators.pv_auth_required
    def new(self, name=None):
        req_args = self.create_request_args(**{
            'method': 'post',
            'url_attr': 'MY_VIDEOS',
            'post_data': {'name': name or pv_constants.VIDEO_NAME}
        })
        return self._api_call(**req_args)

    @pv_decorators.pv_auth_required
    def save(self, video_id, vdd):
        """ Save video with vdd data.

        Args:
            video_id(str): Video identifier to be saved.

        """

        assert isinstance(vdd, dict), 'Simply assure vdd provided is dictionary format.'
        req_args = self.create_request_args(**{
            'method': 'post',
            'url_attr': 'MY_SINGLE_VIDEO',
            'post_data': vdd
        })
        return self._api_call(video_id=video_id, **req_args)

        #self.vdd = {
            #'style': self.style
        #}

        #req_args = {
            #'method':
        #}

from picovico.components import PicovicoVideo
from picovico import constants as pv_constants

class TestVideoComponent:
    def test_video_new(self, mock_obj, video_response, method_calls, pv_request, pv_urls):
        mr = mock_obj.REQUEST
        mr.return_value = video_response.NEW
        pv_video = PicovicoVideo(pv_request.AUTH)
        new_call = method_calls.POST_AUTH.copy()
        new_call.update(url=pv_urls.MY_VIDEOS)
        pv_video.new()
        post_data = {'name': pv_constants.VIDEO_NAME}
        new_call.update(data=post_data)
        mr.assert_called_with(**new_call)
        pv_video.new('Hello Video')
        post_data.update(name='Hello Video')
        mr.assert_called_with(**new_call)
        

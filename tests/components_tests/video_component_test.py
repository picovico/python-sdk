import pytest
from picovico import urls
from picovico import constants as pv_constants
from picovico.components import PicovicoVideo

class TestVideoComponent:
    def test_video_new(self, pv_mocks, pv_request, pv_api_call_args):
        api_call_mock = pv_mocks.API_CALL
        pv_video = PicovicoVideo(pv_request.AUTH)
        new_call = pv_api_call_args.POST.copy()
        new_call.update(path=urls.MY_VIDEOS)
        pv_video.new()
        data = {'name': pv_constants.VIDEO_NAME}
        new_call.update(post_data=data)
        api_call_mock.assert_called_with(**new_call)
        pv_video.new('Hello Video')
        data.update(name='Hello Video')
        api_call_mock.assert_called_with(**new_call)

    @pytest.mark.parametrize('method', ('preview', 'create', 'duplicate'))
    def test_video_id_methods(self, pv_mocks, pv_request, pv_api_call_args, method):
        api_call_mock = pv_mocks.API_CALL
        pv_video = PicovicoVideo(pv_request.AUTH)
        func = getattr(pv_video, method)
        func('video_id')
        call_args = pv_api_call_args.POST.copy()
        url_path = getattr(urls, 'MY_SINGLE_VIDEO_{}'.format(method.upper()))
        url_path = url_path.format(video_id='video_id')
        call_args.update(path=url_path)
        api_call_mock.assert_called_with(**call_args)

    def test_video_save(self, pv_mocks, pv_request, pv_api_call_args):
        api_call_mock = pv_mocks.API_CALL
        pv_video = PicovicoVideo(pv_request.AUTH)
        vdd={'some_vdd': 'data'}
        pv_video.save('video_id', vdd)
        call_args = pv_api_call_args.POST.copy()
        call_args.update(path=urls.MY_SINGLE_VIDEO.format(video_id='video_id'))
        call_args.update(post_data=vdd)
        api_call_mock.assert_called_with(**call_args)


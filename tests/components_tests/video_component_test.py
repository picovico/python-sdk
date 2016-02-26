from picovico.components import PicovicoVideo

class TestVideoComponent:
    def test_video_new(self, mocker, video_response, method_calls, pv_request, pv_urls):
        mr = mocker.patch('picovico.baserequest.requests.request')
        mr.return_value = video_response.NEW
        pv_video = PicovicoVideo(pv_request.AUTH)
        new_call = method_calls.POST.copy()
        new_call.update(url=pv_urls.MY_VIDEOS)
        pv_video.new()
        mr.assert_called_with(**new_call)

from picovico.components import PicovicoPhoto

class TestMusicComponent:
    def test_upload_url(self, mock_obj, pv_request, method_calls, pv_urls):
        mr = mock_obj.REQUEST
        post_call = method_calls.POST_AUTH.copy()
        ph_comp = PicovicoPhoto(pv_request.AUTH)
        args = ("something", "something_thumb")
        ph_comp.upload_url(*args)
        post_call.update(url=pv_urls.MY_PHOTOS)
        post_call.update(data=dict(zip(('url', 'thumbnail_url'), args)))
        mr.assert_called_with(**post_call)


from picovico import urls
from picovico.components import PicovicoPhoto


class TestMusicComponent:
    def test_upload_url(self, pv_mocks, pv_request, pv_api_call_args):
        api_call_mock = pv_mocks.API_CALL
        post_call = pv_api_call_args.POST.copy()
        ph_comp = PicovicoPhoto(pv_request.AUTH)
        args = ("something", "something_thumb")
        ph_comp.upload_url(*args)
        post_call.update(path=urls.MY_PHOTOS)
        post_call.update(post_data=dict(zip(('url', 'thumbnail_url'), args)))
        api_call_mock.assert_called_with(**post_call)


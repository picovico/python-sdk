from six.moves.urllib import parse
from picovico.components import PicovicoPhoto
from picovico.baserequest import PicovicoRequest
from picovico import urls as pv_urls

class TestPhotoComponent:
    def test_create_request_args(self):
        req_args = PicovicoPhoto.create_request_args(music_id='hello')
        assert 'music_id' in req_args

    def test_upload_url(self, request_mock, headers, response, method_calls):
        request_mock.return_value = response.SUCCESS.OK
        post_request = method_calls.POST.copy()
        auth_header = headers.AUTH.copy()
        req = PicovicoRequest(auth_header)
        ph_comp = PicovicoPhoto(req)
        assert ph_comp.component == 'photo'
        args = ("something", "something_thumb")
        ph_comp.upload_url(*args)
        post_request.update(url=parse.urljoin(pv_urls.PICOVICO_BASE, pv_urls.MY_PHOTOS))
        post_request.update(data=dict(zip(('url', 'thumbnail_url'), args)))
        post_request.update(headers=auth_header)
        request_mock.assert_called_with(**post_request)


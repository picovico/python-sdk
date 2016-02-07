import mock
import pytest
from six.moves.urllib import parse
from picovico.components import *
from picovico.baserequest import PicovicoRequest
from picovico import urls as pv_urls

class TestPhotoComponent:
    def test_upload_url(self, response_messages, success_response, method_calls):
        post_request = method_calls.get('post').copy()
        auth_header = response_messages.get('valid_auth_header').copy()
        req = PicovicoRequest(auth_header)
        ph_comp = PicovicoPhoto(req)
        assert ph_comp.component == 'photo'
        with mock.patch('picovico.baserequest.requests.request') as mr:
            mr.return_value = success_response
            args = ("something", "something_thumb")
            ph_comp.upload_photo_url(*args)
            post_request.update(url=parse.urljoin(pv_urls.PICOVICO_BASE, pv_urls.MY_PHOTO))
            post_request.update(data=dict(zip(('url', 'thumbnail_url'), args)))
            post_request.update(headers=auth_header)
            mr.assert_called_with(**post_request)


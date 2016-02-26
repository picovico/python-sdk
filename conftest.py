import collections

import six
import pytest
import requests
import mock

from picovico.baserequest import PicovicoRequest
from picovico import urls 

urljoin = six.moves.urllib.parse.urljoin

def _create_namedtuple(name, dict_to_make):
    key_transformation = {k.upper(): v for k, v in six.iteritems(dict_to_make)}
    Factory = collections.namedtuple(name, six.iterkeys(key_transformation))
    return Factory(**key_transformation)


def _create_request(auth=False):
    headers = None
    if auth:
        headers = {'X-Access-Key': "key", 'X-Access-Token': "token"}
    return PicovicoRequest(headers)

@pytest.fixture()
def pv_urls():
    url = {k: urljoin(urls.PICOVICO_BASE, getattr(urls, k)) for k in dir(urls) if not k.startswith('_')}
    return _create_namedtuple('PicovicoURL', url)

@pytest.fixture()
def headers():
    headers = {
        'auth': {'X-Access-Key': "key", 'X-Access-Token': "token"},
        'invalid': "Invalid",
        'valid': {'X-VALID': "This is valid header."},
    }
    return _create_namedtuple('FakeHeader', headers)

@pytest.fixture()
def video_msg():
    msg = {
        'new': {'id': "NEWVIDEO"}
    }
    return _create_namedtuple('FakeVideoMsg', msg)

@pytest.fixture()
def messages():
    error_msg = {
        'bad': {'error': {'status': 400, 'message': "This is bad request error."}},
        'notfound': {'error': {'status': 404, 'message': "This is not found error."}},
        'auth': {'error': {'status': 401, 'message': "This is unauthorized error."}},
        'random': {'status':415, 'message': "This is some error"},
        'server': {'error': {'status': 501, 'message': "This is server error."}}
    }
    error_msg = _create_namedtuple('ErrorMsg', error_msg)
    success_msg = {
        'ok': {'message': "This is success response."},
        'auth': {'access_key': "valid_key", 'access_token': "valid_token"},
    }
    success_msg = _create_namedtuple('SuccessMsg', success_msg)
    
    m = {
        'success': success_msg,
        'error': error_msg,
    }
    #m = {
        #'server_error': {'error': {'status': 501, 'message': "This is server error."}},
        #'error': {'error': {'status': 400, 'message': "This is bad request error."}},
        #'auth_error': {'error': {'status': 401, 'message': "This is unauthorized error."}},
        #'notfound_error': {'error': {'status': 404, 'message': "This is not found error."}},
        #'some_error': {'status':415, 'message': "This is some error"},
        #'success': {'message': "This is success response."},
        #'success_auth': {'access_key': "valid_key", 'access_token': "valid_token"},
        #'valid_header': {'X-VALID': "This is valid header."},
        #'valid_auth_header': {'X-Access-Key': "key", 'X-Access-Token': "token"},
        #'invalid_header': "Invalid",
        #'new_video': {'id': "NEWVIDEO"}
    #}
    return _create_namedtuple('FakeResponseMsg', m)

def create_response(status_code, json_value):
    res = requests.Response()
    res.json = mock.MagicMock()
    res.status_code = status_code
    res.json.return_value = json_value
    return res

#@pytest.fixture()
#def success_response(response_messages):
    #res = create_response(200, response_messages['success'])
    #return res

#@pytest.fixture()
#def auth_response(response_messages):
    #res = create_response(200, response_messages['success_auth'])
    #return res

#@pytest.fixture()
#def error_response(response_messages):
    #res = create_response(400, response_messages['bad'])
    #return res

def create_fp(content):
    gfp = six.StringIO()
    gfp.writelines(content)
    gfp.seek(0)
    return gfp

@pytest.fixture()
def method_calls():
    gm = {
        'get': {'method': 'get', 'url': None},
        'post': {'method': 'post', 'url': None},
        'put': {'method': 'put', 'url': None},
        'delete': {'method': 'delete', 'url': None},
    }
    return _create_namedtuple('FakeMethodArgs', gm)

@pytest.fixture()
def profile_fp():
    fp = {
        'default': create_fp(('[DEFAULT]\n', 'APP_ID=default_app_id\n',)),
        'other': create_fp(('[OTHER]\n', 'APP_ID=other_app_id\n',))
    }
    return _create_namedtuple('FakeProfileFiles', fp)
    #gfp = six.StringIO()
    #gfp.writelines()
    #gfp.seek(0)
    #return gfp

#@pytest.fixture()
#def profile_fp_other():
    #gfp = six.StringIO()
    #gfp.writelines(('[OTHER]\n', 'APP_ID=other_app_id\n',))
    #gfp.seek(0)
    #return gfp
@pytest.fixture()
def video_response(video_msg):
    vid_resp = {
        'new': create_response(200, video_msg.NEW)
    }
    return _create_namedtuple('FakeVideoResponse', vid_resp)
    
@pytest.fixture()
def response(messages, video_response):
    ok_resp = {
        'ok': create_response(200, messages.SUCCESS.OK),
        'auth': create_response(200, messages.SUCCESS.AUTH),
        'video': video_response
    }
    ok_resp = _create_namedtuple('SuccessResponse', ok_resp)
    error_resp = {
        'bad': create_response(400, messages.ERROR.BAD),
    }
    error_resp = _create_namedtuple('ErrorResponse', error_resp)
    res = {
        'success': ok_resp,
        'error': error_resp
    }
    return _create_namedtuple('FakeResponse', res)

@pytest.fixture
def pv_request():
    req = {
        'auth': _create_request(True),
        'noauth': _create_request()
    }
    return _create_namedtuple('FakeRequest', req)

import copy

import pytest
import requests
import mock



@pytest.fixture()
def response_messages():
    m = {
        'server_error': {'error': {'status': 501, 'message': "This is server error."}},
        'bad_error': {'error': {'status': 400, 'message': "This is bad request error."}},
        'auth_error': {'error': {'status': 401, 'message': "This is unauthorized error."}},
        'notfound_error': {'error': {'status': 404, 'message': "This is not found error."}},
        'some_error': {'status':415, 'message': "This is some error"},
        'success': {'message': "This is success response."},
        'success_auth': {'access_key': "valid_key", 'access_token': "valid_token"},
        'valid_header': {'X-VALID': "This is valid header."},
        'valid_auth_header': {'X-Access-Key': "key", 'X-Access-Token': "token"},
        'invalid_header': "Invalid",
    }
    return m

def create_response(status_code, json_value):
    res = requests.Response()
    res.json = mock.MagicMock()
    res.status_code = status_code
    res.json.return_value = json_value
    return res

@pytest.fixture()
def success_response(response_messages):
    res = create_response(200, response_messages['success'])
    return res

@pytest.fixture()
def auth_response(response_messages):
    res = create_response(200, response_messages['success_auth'])
    return res

@pytest.fixture()
def error_response(response_messages):
    res = create_response(400, response_messages['bad'])
    return res

@pytest.fixture()
def method_calls():
    gm = {
        'get': {'method': 'get', 'url': None},
        'post': {'method': 'post', 'url': None},
        'put': {'method': 'put', 'url': None},
        'delete': {'method': 'delete', 'url': None},
    }
    return gm

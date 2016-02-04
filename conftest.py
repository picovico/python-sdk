import pytest
import requests
import mock


@pytest.fixture()
def basic_errors():
    return {
        'server': {'error': {'status': 501, 'message': "This is server error."}},
        'bad': {'error': {'status': 400, 'message': "This is bad request error."}},
        'auth': {'error': {'status': 401, 'message': "This is unauthorized error."}},
        'notfound': {'error': {'status': 404, 'message': "This is not found error."}},
        'some': {'status':415, 'message': "This is some error"}
    }

@pytest.fixture()
def success_message():
    return {
        'generic': {'message': "This is success response."},
        'auth': {'access_key': "valid_key", 'access_token': "valid_token"}
    }

@pytest.fixture()
def headers():
    return {
        'valid': {'X-VALID': "This is valid header."},
        'invalid': "This is invalid header."
    }

def create_response(status_code, json_value):
    res = requests.Response()
    res.json = mock.MagicMock()
    res.status_code = status_code
    res.json.return_value = json_value
    return res

@pytest.fixture()
def success_response(success_message):
    res = create_response(200, success_message['generic'])
    return res

@pytest.fixture()
def auth_response(success_message):
    res = create_response(200, success_message['auth'])
    return res

@pytest.fixture()
def error_response(basic_errors):
    res = create_response(400, basic_errors['bad'])
    return res

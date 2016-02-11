import pytest
from picovico import session

class TestPicovicoSession:
    def test_properties(self):
        pv_session = session.PicovicoSessionMixin('app_id', 'app_secret')
        assert pv_session.app_id == 'app_id'
        assert pv_session.app_secret == 'app_secret'
        with pytest.raises(AttributeError):
            #Donot allow to set app  id
            pv_session.app_id =  None
        assert pv_session.device_id == session.DEFAULT_DEVICE_ID
        pv_session.device_id = "my_new_device_id"
        assert pv_session.device_id != session.DEFAULT_DEVICE_ID
        assert pv_session.device_id == "my_new_device_id"
        assert pv_session.headers is None
        pv_session.set_access_tokens("access_key", "access_token")
        assert pv_session.access_token == "access_token"
        assert pv_session.access_key == "access_key"
        with pytest.raises(AttributeError):
            #donot allow override of tokens and auth_header
            pv_session.access_key = "new_access_token"
        with pytest.raises(AttributeError):
            pv_session.access_token = "new_access_key"
        with pytest.raises(AttributeError):
            pv_session.headers = None
        assert pv_session.headers is not None


    def test_anonymous_vs_logged_in(self):
        pv_session = session.PicovicoSessionMixin('app_id', 'app_secret')
        assert pv_session.is_anonymous()
        assert not pv_session.is_authorized()
        pv_session.set_access_tokens('access_key', 'access_token')
        assert not pv_session.is_anonymous()
        assert pv_session.is_authorized()



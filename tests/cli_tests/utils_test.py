import sys
import itertools

try:
    import mock
except ImportError:
    from unittest import mock
import pytest

from picovico import PicovicoAPI
from picovico.cli import profile_utils
from picovico.cli import utils as pv_utils
from picovico.cli.profile_utils import DEFAULT_PROFILE_NAME 
    
def get_mocked_profile():
    msess = mock.Mock()
    for info in range(2):
        yield msess
        

class TestPVCLIUtils:
    @pytest.mark.parametrize('profile_name,session,func', itertools.product((None, 'Hello'),(True, False), ('authenticate', 'login')))
    def test_prepare_api_objects(self, mocker, profile_name, session, func):
        prof = mocker.Mock()
        prof.NAME = profile_name or DEFAULT_PROFILE_NAME
        prof.APP_ID = 'APP_ID'
        prof.DEVICE_ID = profile_name
        mgp = mocker.patch('picovico.cli.utils.profile_utils.get_profile', return_value=prof)
        mapi = mocker.MagicMock(spec=PicovicoAPI)
        mocker.patch('picovico.cli.utils.PicovicoAPI', return_value=mapi)
        #mapi.set_access_tokens = mocker.Mock()
        if not session:
            pv_utils.prepare_api_object(profile_name, session)
            mgp.assert_called_with(prof.NAME, info=True)
        else:
            sess = mocker.Mock()
            mgsi = mocker.patch('picovico.cli.utils.profile_utils.get_session_info', return_value=sess)
            sess.PROFILE = prof.NAME
            sess.ACCESS_KEY = 'access_key'
            sess.ACCESS_TOKEN = 'access_token'
            pv_utils.prepare_api_object(profile_name, session)
            #print sess.called
            mapi.set_access_tokens.assert_called_with('access_key', 'access_token')
            mgsi.return_value = None
            mauth = mocker.patch('picovico.cli.utils.profile_utils.get_auth_names')
            mauth.return_value = None
            mns = mocker.patch('picovico.cli.utils.prompt.show_no_session')
            def side_effect(*args, **kwargs):
                if prof.NAME in args:
                    sys.exit(0)
            mns.side_effect = side_effect
            with pytest.raises(SystemExit):
                pv_utils.prepare_api_object(profile_name, session)
            mns.assert_called_with(prof.NAME)
            auth_name = getattr(profile_utils, '{}_INFO'.format(func.upper()))
            mauth.return_value = auth_name
            for n in auth_name:
                setattr(prof, n, None)
            with pytest.raises(SystemExit):
                pv_utils.prepare_api_object(profile_name, session)
            mns.assert_called_with(prof.NAME)
            for n in auth_name:
                setattr(prof, n, n.lower())
            mact = mocker.patch('picovico.cli.utils.auth_action')
            pv_utils.prepare_api_object(profile_name, session)
            argument = {k.lower(): getattr(prof, k) for k in auth_name}
            mact.assert_called_with(func, prof.NAME, **argument)
    
    @pytest.mark.parametrize('profile,func', itertools.product((None, 'hello'), ('login', 'authenticate')))
    def test_auth_action(self, mocker, profile, func):
        mapi = mocker.MagicMock(spec=PicovicoAPI)
        mocker.patch('picovico.cli.utils.prepare_api_object', return_value=mapi)
        data = {
            'ACCESS_KEY': 'access_key',
            'ACCESS_TOKEN': 'access_token',
            'PROFILE': profile or DEFAULT_PROFILE_NAME
        }
        mws = mocker.patch('picovico.cli.utils.file_utils.write_to_session_file')
        mapi.is_authorized.return_value = False
        pv_utils.auth_action(func, profile)
        mws.assert_not_called()
        mapi.is_authorized.return_value = True
        for k in data:
            if '_' in k:
                setattr(mapi, k.lower(), data[k])
        pv_utils.auth_action(func, profile)
        mws.assert_called_with(data)

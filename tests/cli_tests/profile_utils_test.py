import itertools
import six
import pytest

from picovico.cli import profile_utils

ConfigParser = six.moves.configparser.SafeConfigParser

default_section_name = profile_utils.DEFAULT_PROFILE_NAME
#input_args = ('Enter Application Id provided: ',
            #'Enter Device Identifier->[default:{}]: '.format(cli.DEFAULT_DEVICE_ID),
            #'Enter Application Secret: ',
            #'Enter Picovico Username: ',
            #'Enter Picovico Password[Will not be stored]: ')
return_args = ('MY_APP_ID', None, 'MY_APP_SECRET',
                    'MY_USERNAME', 'MY_PASSWORD')
profiles = (default_section_name, 'NONDEFAULT')
#return_value = dict(six.moves.zip(input_args, return_args))

#def configure_mocked(*args, **kwargs):
    #if args[0] in return_value:
        #return return_value.get(args[0])
def mocked_cfg(mocker):
    return mocker.MagicMock(spec=ConfigParser)

class TestCliProfileUtils:
    @pytest.mark.parametrize('ret_val', [True, False])
    def test_check_against_factory(self, mocker, ret_val):
        cfg = mocked_cfg(mocker)
        cfg.has_section.return_value = ret_val
        cfg.has_option.return_value = ret_val
        if ret_val:
            assert profile_utils.check_against_factory(cfg, default_section_name, range(1))
            cfg.has_option.assert_called_with(default_section_name, 0)
            assert profile_utils.check_against_factory(cfg, 'NONDEFAULT', range(1))
            cfg.has_section.assert_called_with('NONDEFAULT')
        else:
            assert not profile_utils.check_against_factory(cfg, 'NONDEFAULT', range(1))
            assert not profile_utils.check_against_factory(cfg, default_section_name, range(1))
        cfg.get.return_value = ret_val
        if ret_val:
            assert profile_utils.check_against_factory(cfg, 'NONDEFAULT', range(1), ret_val)
            cfg.get.assert_called_with('NONDEFAULT', 0)
        else:
            assert not profile_utils.check_against_factory(cfg, 'NONDEFAULT', range(1), True)

    @pytest.mark.parametrize('profile, ret_val', itertools.product(profiles, (True, False)))
    def test_check_against_funcs(self, mocker, profile, ret_val):
        against = None
        def side_effect(*args, **kwargs):
            assert args[0] in profiles
            assert args[1] in against
            return ret_val
        cfg = mocked_cfg(mocker)
        cfg.has_section.return_value = ret_val
        cfg.has_option.side_effect = side_effect
        cfg.get.return_value = side_effect
        against = profile_utils.NECESSARY_INFO
        profile_utils.has_necessary_info(cfg, profile)
        if profile != default_section_name:
            cfg.has_section.assert_called_with(profile)
        assert profile_utils.check_necessary_info_values(cfg, profile) == ret_val
        against = profile_utils.LOGIN_INFO if ret_val else profile_utils.LOGIN_INFO[:1]
        assert profile_utils.has_login_info(cfg, profile) == ret_val
        assert profile_utils.has_login_info(cfg, profile, both=ret_val) == ret_val
        assert profile_utils.check_login_info_value(cfg, profile) == ret_val
        assert profile_utils.check_login_info_value(cfg, profile, both=ret_val) == ret_val
        against = profile_utils.AUTHENTICATE_INFO
        assert profile_utils.has_authenticate_info(cfg, profile) == ret_val
        assert profile_utils.check_authenticate_info_value(cfg, profile) == ret_val


    _funcs = ('authenticate', 'login')

    @pytest.mark.parametrize('func,no_func', [_funcs, _funcs[::-1]])
    def test_get_auth_names(self, mocker, func, no_func):
        val = False
        def side_effect(*args, **kwargs):
            if 'both' in kwargs:
                return val
            else:
                return True
        cfg = mocker.MagicMock(spec=ConfigParser)
        mocker.patch('picovico.cli.profile_utils.get_raw_profile', return_value=cfg)
        mock_one = mocker.patch('picovico.cli.profile_utils.check_'+func+'_info_value')
        mock_two = mocker.patch('picovico.cli.profile_utils.check_'+no_func+'_info_value')
        mock_one.return_value = True
        assert profile_utils.get_auth_names(default_section_name) == getattr(profile_utils, '{}_INFO'.format(func.upper()))
        if func == 'authenticate':
            mock_two.assert_not_called()
        if func == 'login':
            mock_one.side_effect = side_effect
            for v in range(2):
                val = bool(v)
                check_val = profile_utils.LOGIN_INFO[:1] if not val else profile_utils.LOGIN_INFO
                assert profile_utils.get_auth_names(default_section_name) == check_val

    @pytest.mark.parametrize('func,auth_name', [('authenticate', None), ('login', None), ('authenticate', profile_utils.AUTHENTICATE_INFO), ('login', profile_utils.LOGIN_INFO), ('login', profile_utils.LOGIN_INFO[:1])])
    def test_get_auth_check_and_removal(self, mocker, func, auth_name):
        def side_effect(*args, **kwargs):
            mocked_p = mocker.MagicMock()
            if auth_name:
                for name in auth_name:
                    setattr(mocked_p, name, True)
                if len(auth_name) == 1 and 'USERNAME' in auth_name:
                    setattr(mocked_p, 'PASSWORD', None)
            return mocked_p
        mocker.patch('picovico.cli.profile_utils.get_auth_names', return_value=auth_name)
        mp = mocker.patch('picovico.cli.profile_utils.get_profile')
        mp.side_effect = side_effect
        kargs, rem, names  = profile_utils.get_auth_check_and_removal(func, default_section_name)
        if auth_name is None:
            assert all(k in kargs and kargs[k] for k in ('do_prompt', 'profile'))
            assert rem is None
        else:
            assert any(k.lower() in kargs and kargs[k.lower()] for k in auth_name)
            rem_check = 'APP_SECRET' if func == 'login' else 'USERNAME'
            assert rem == rem_check
            assert names.index(func)
        assert all(k in names for k in self._funcs)



        #mock_one.return_value = True
        #mock_two.return_value = False

    #def test_set_profile(self, mocker):
        #cfg = mocked_cfg(mocker)
        #mocker.patch('picovico.cli.profile_utils.file_utils.get_file_obj')
        #for val in profile_val:
            #for ret_val in profile_val[val]:
                #cfg.has_section.return_value = ret_val
                #cfg.has_option.return_value = ret_val
                #cfg.get.return_value = ret_val
    #def test_has_necessary_configs(self, pv_profile_fp):
        #default_fp = pv_profile_fp.DEFAULT
        #cfg = six.moves.configparser.SafeConfigParser()
        #cfg.readfp(default_fp)
        #assert not profile_utils.has_necessary_info(cfg, default_section_name)
        #assert not profile_utils.check_necessary_info_values(cfg, default_section_name)
        #default_fp.write('DEVICE_ID=device_id\n')
        #default_fp.seek(0)
        #cfg.readfp(default_fp)
        #assert profile_utils.has_necessary_info(cfg, default_section_name)
        #assert profile_utils.check_necessary_info_values(cfg, default_section_name)

    #def test_optional_configs(self, default_fp):
        #cfg = six.moves.configparser.SafeConfigParser()
        #cfg.readfp(default_fp)
        #with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            #cli.has_optional_secret_configs(cfg)
        #assert exc.value.code == 5
        #with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            #cli.has_optional_username_configs(cfg)
        #assert exc.value.code == 5
        #with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            #cli.has_optional_configs(cfg,both=True)
        #assert exc.value.code == 5
        #default_fp.write('APP_SECRET=app_secret\n')
        #default_fp.seek(0)
        #cfg.readfp(default_fp)
        #assert cli.has_optional_secret_configs(cfg)
        #with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            #cli.has_optional_username_configs(cfg)
        #assert cli.has_optional_configs(cfg)
        #up = ('[DEFAULT]\n', 'ACCESS_KEY=access_key\n', 'ACCESS_TOKEN=access_token\n')
        #default_fp.write(up[1])
        #default_fp.seek(0)
        #cfg.readfp(default_fp)
        #with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            #cli.has_optional_token_configs(cfg)
        #default_fp.write(up[2])
        #default_fp.seek(0)
        #cfg.readfp(default_fp)
        #assert cli.has_optional_token_configs(cfg)
        #cfg = six.moves.configparser.SafeConfigParser()
        #fp = six.StringIO()
        #fp.writelines(up[0]+('USERNAME=username\n'))
        #fp.seek(0)
        #cfg.readfp(fp)
        #with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            #cli.has_optional_secret_configs(cfg)
        #assert cli.has_optional_configs(cfg)

    #def test_get_configure_profile(self, mocker):
        #basic_values = ('APP_ID', 'DEVICE_ID', 'SECTION')
        #m = mocker.patch('picovico.clidriver.six.moves.input')
        #m.side_effect = configure_mocked
        #profile_info = cli.get_configure_profile()
        #assert profile_info.APP_ID == return_args[0]
        #assert profile_info.DEVICE_ID == cli.DEFAULT_DEVICE_ID
        #assert profile_info.SECTION == cli.DEFAULT_SECTION_NAME
        #for attr in profile_info._fields:
            #if attr not in basic_values:
                #assert getattr(profile_info, attr) is None
        #return_value.update({input_args[1]:'MY_DEVICE_ID'})
        #profile_info = cli.get_configure_profile()
        #assert profile_info.DEVICE_ID != cli.DEFAULT_DEVICE_ID
        #assert profile_info.DEVICE_ID == 'MY_DEVICE_ID'
        #profile_info = cli.get_configure_profile('New Profile')
        #assert profile_info.SECTION != cli.DEFAULT_SECTION_NAME
        #profile_info = cli.get_configure_profile(auth=True)
        #assert profile_info.APP_SECRET is not None
        #assert profile_info.APP_SECRET == return_args[2]
        #assert profile_info.USERNAME is None
        #assert profile_info.PASSWORD is None
        #profile_info = cli.get_configure_profile(login=True)
        #assert profile_info.APP_SECRET is None
        #assert profile_info.USERNAME is not None
        #assert profile_info.PASSWORD is not None
        #profile_info = cli.get_configure_profile(login=True, auth=True)
        #assert profile_info.APP_SECRET is None
        #assert profile_info.USERNAME is None
        #assert profile_info.PASSWORD is None
        #assert profile_info.AUTH is None

    #def test_create_conf_values(self):
        #value_to_test = (('MY_ATTR', 'MY_VALUE'),)
        #values = profile_utils.create_profile_values(value_to_test)
        #for val in values:
            #assert val.NAME == value_to_test[0][0]
            #assert val.VALUE == value_to_test[0][1]

    #def test_get_profile(self, mocker, pv_profile_fp):
        #default_fp = pv_profile_fp.DEFAULT
        #other_fp = pv_profile_fp.OTHER
        #cfg = six.moves.configparser.SafeConfigParser()
        #cfg.readfp(default_fp)
        #m = mocker.patch('picovico.cli.profile_utils.get_raw_profile')
        #m.return_value = cfg
        #config = profile_utils.get_profile(default_section_name, info=False)
        #assert config.APP_ID == 'default_app_id'
        #cfg.readfp(other_fp)
        #mocker.stopall()
        #m = mocker.patch('picovico.cli.profile_utils.get_raw_profile')
        #m.return_value = cfg
        #config = profile_utils.get_profile('OTHER', info=False)
        #assert config.APP_ID == 'other_app_id'

    #def test_set_profile(self, mocker, pv_profile_fp):
        #default_fp = pv_profile_fp.DEFAULT
        #other_fp = pv_profile_fp.OTHER
        #cfg = six.moves.configparser.SafeConfigParser()
        #cfg.readfp(default_fp)
        #old_cfg = cfg.items(default_section_name)
        #with pytest.raises(six.moves.configparser.NoOptionError):
           #cfg.get(default_section_name, 'DEVICE_ID')
        #values = profile_utils.create_profile_values(((a, return_args[i]) for i, a in enumerate(profile_utils.NECESSARY_INFO)))
        #mocker.patch('picovico.cli.file_utils.get_profile_file')
        #mocker.patch('picovico.cli.file_utils.get_file_obj')
        #m = mocker.patch('picovico.cli.profile_utils.get_raw_profile')
        #m.return_value = cfg
        #profile_utils.set_profile(values, default_section_name)
        #assert old_cfg != cfg.items(default_section_name)
        #assert cfg.get(default_section_name, 'DEVICE_ID')

    #def test_check_session_file(self, mocker):
        #data = {'ACCESS_KEY': 'my_access_key', 'ACCESS_TOKEN': 'my_access_token'}
        #mocker.patch('picovico.cli.file_utils.get_session_file')
        #mr = mocker.patch('picovico.cli.file_utils.open')
        #e = IOError()
        #e.errno = errno.ENOENT
        #mr.side_effect = e
        #assert not profile_utils.check_session_file()
        #e.errno = errno.EIO
        #with pytest.raises(IOError):
            #profile_utils.check_session_file()
        #mocker.stopall()
        #mr = mocker.patch('picovico.cli.file_utils.read_from_session_file')
        #mr.return_value = data
        #assert not profile_utils.check_session_file()
        #data.update(ID=1, PROFILE='default')
        #assert profile_utils.check_session_file()
        #data.update(ID=None, PROFILE=None)
        #assert not profile_utils.check_session_file()
    #def test_write_access_info(self, mocker):
        #profiles = {k: None for k in cli.Profile._fields}
        #profiles.update({
            #'SECTION': cli.DEFAULT_SECTION_NAME,
            #'AUTH': True,
            #'APP_ID': 'MY_APP_ID',
            #'APP_SECRET': 'MY_APP_SECRET'
        #})
        #token_returns = ('MY_ACCESS_KEY', 'MY_ACCESS_TOKEN')
        #profile = cli.Profile(**profiles)
        #mocker.patch('picovico.PicovicoAPI.login')
        #mocker.patch('picovico.PicovicoAPI.authenticate')
        #mocker.patch('picovico.PicovicoAPI.set_access_tokens')
        #mocker.patch('picovico.PicovicoAPI.access_key', new_callabale=mock.PropertyMock, return_value=token_returns[0])
        #mocker.patch('picovico.PicovicoAPI.access_token', new_callable=mock.PropertyMock, return_value=token_returns[1])
        #pc = mocker.patch('picovico.clidriver.set_configs')
        #def set_config_side_effect(*args, **kwargs):
            #argument = args[0]
            #if len(argument) > 1:
                #assert all(getattr(a, 'attr') in cli.OPTIONAL_INFO_TOKEN for a in argument)
                #for i, a in enumerate(argument):
                    #if getattr(a, 'attr') == cli.OPTIONAL_INFO_TOKEN[i]:
                        #if isinstance(getattr(a, 'value'), six.string_types):
                            #assert getattr(a, 'value') == token_returns[i]
                        #else:
                            #Due to some odd behaviour in mock
                            #assert getattr(a, 'value').return_value == token_returns[i]
            #else:
                #assert getattr(argument[0], 'attr') == 'APP_SECRET'
                #assert getattr(argument[0], 'value') == profile.APP_SECRET
        #pc.side_effect = set_config_side_effect
        #cli.write_access_info(profile)

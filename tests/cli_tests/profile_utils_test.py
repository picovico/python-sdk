#import os
import contextlib
import errno

import six
import pytest
#import mock

#from picovico import exceptions as pv_exceptions
from picovico.cli import profile_utils


default_section_name = profile_utils.DEFAULT_PROFILE_NAME
#input_args = ('Enter Application Id provided: ',
            #'Enter Device Identifier->[default:{}]: '.format(cli.DEFAULT_DEVICE_ID),
            #'Enter Application Secret: ',
            #'Enter Picovico Username: ',
            #'Enter Picovico Password[Will not be stored]: ')
return_args = ('MY_APP_ID', None, 'MY_APP_SECRET',
                    'MY_USERNAME', 'MY_PASSWORD')
#return_value = dict(six.moves.zip(input_args, return_args))

#def configure_mocked(*args, **kwargs):
    #if args[0] in return_value:
        #return return_value.get(args[0])

class TestCliProfileUtils:
    def test_has_necessary_configs(self, profile_fp_default):
        cfg = six.moves.configparser.SafeConfigParser()
        cfg.readfp(profile_fp_default)
        assert not profile_utils.has_necessary_info(cfg, default_section_name)
        assert not profile_utils.check_necessary_info_values(cfg, default_section_name)
        profile_fp_default.write('DEVICE_ID=device_id\n')
        profile_fp_default.seek(0)
        cfg.readfp(profile_fp_default)
        assert profile_utils.has_necessary_info(cfg, default_section_name)
        assert profile_utils.check_necessary_info_values(cfg, default_section_name)

    #def test_optional_configs(self, profile_fp_default):
        #cfg = six.moves.configparser.SafeConfigParser()
        #cfg.readfp(profile_fp_default)
        #with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            #cli.has_optional_secret_configs(cfg)
        #assert exc.value.code == 5
        #with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            #cli.has_optional_username_configs(cfg)
        #assert exc.value.code == 5
        #with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            #cli.has_optional_configs(cfg,both=True)
        #assert exc.value.code == 5
        #profile_fp_default.write('APP_SECRET=app_secret\n')
        #profile_fp_default.seek(0)
        #cfg.readfp(profile_fp_default)
        #assert cli.has_optional_secret_configs(cfg)
        #with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            #cli.has_optional_username_configs(cfg)
        #assert cli.has_optional_configs(cfg)
        #up = ('[DEFAULT]\n', 'ACCESS_KEY=access_key\n', 'ACCESS_TOKEN=access_token\n')
        #profile_fp_default.write(up[1])
        #profile_fp_default.seek(0)
        #cfg.readfp(profile_fp_default)
        #with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            #cli.has_optional_token_configs(cfg)
        #profile_fp_default.write(up[2])
        #profile_fp_default.seek(0)
        #cfg.readfp(profile_fp_default)
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

    def test_create_conf_values(self):
        value_to_test = (('MY_ATTR', 'MY_VALUE'),)
        values = profile_utils.create_profile_values(value_to_test)
        for val in values:
            assert val.NAME == value_to_test[0][0]
            assert val.VALUE == value_to_test[0][1]

    def test_get_profile(self, mocker, profile_fp_default, profile_fp_other):
        cfg = six.moves.configparser.SafeConfigParser()
        cfg.readfp(profile_fp_default)
        m = mocker.patch('picovico.cli.profile_utils.get_raw_profile')
        m.return_value = cfg
        config = profile_utils.get_profile(default_section_name, info=False)
        assert config.APP_ID == 'default_app_id'
        cfg.readfp(profile_fp_other)
        mocker.stopall()
        m = mocker.patch('picovico.cli.profile_utils.get_raw_profile')
        m.return_value = cfg
        config = profile_utils.get_profile('OTHER', info=False)
        assert config.APP_ID == 'other_app_id'

    def test_set_profile(self, mocker, profile_fp_default, profile_fp_other):
        cfg = six.moves.configparser.SafeConfigParser()
        cfg.readfp(profile_fp_default)
        old_cfg = cfg.items(default_section_name)
        with pytest.raises(six.moves.configparser.NoOptionError):
           cfg.get(default_section_name, 'DEVICE_ID')
        values = profile_utils.create_profile_values(((a, return_args[i]) for i, a in enumerate(profile_utils.NECESSARY_INFO)))
        mocker.patch('picovico.cli.file_utils.get_profile_file')
        mocker.patch('picovico.cli.file_utils.get_file_obj')
        m = mocker.patch('picovico.cli.profile_utils.get_raw_profile')
        m.return_value = cfg
        profile_utils.set_profile(values, default_section_name)
        assert old_cfg != cfg.items(default_section_name)
        assert cfg.get(default_section_name, 'DEVICE_ID')

    def test_check_session_file(self, mocker):
        data = {'ACCESS_KEY': 'my_access_key', 'ACCESS_TOKEN': 'my_access_token'}
        mocker.patch('picovico.cli.file_utils.get_session_file')
        mr = mocker.patch('picovico.cli.file_utils.open')
        e = IOError()
        e.errno = errno.ENOENT
        mr.side_effect = e
        assert not profile_utils.check_session_file()
        e.errno = errno.EIO
        with pytest.raises(IOError):
            profile_utils.check_session_file()
        mocker.stopall()
        mr = mocker.patch('picovico.cli.file_utils.read_from_session_file')
        mr.return_value = data
        assert not profile_utils.check_session_file()
        data.update(ID=1, PROFILE='default')
        assert profile_utils.check_session_file()
        data.update(ID=None, PROFILE=None)
        assert not profile_utils.check_session_file()
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

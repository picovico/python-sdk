import os
import errno

import six
import pytest
import mock

from picovico import exceptions as pv_exceptions
from picovico import clidriver as cli

input_args = ('Enter Application Id provided: ',
            'Enter Device Identifier->[default:{}]: '.format(cli.DEFAULT_DEVICE_ID),
            'Enter Application Secret: ',
            'Enter Picovico Username: ',
            'Enter Picovico Password[Will not be stored]: ')
return_args = ('MY_APP_ID', None, 'MY_APP_SECRET',
                    'MY_USERNAME', 'MY_PASSWORD')
return_value = dict(six.moves.zip(input_args, return_args))

def configure_mocked(*args, **kwargs):
    #import pdb
    #pdb.set_trace()
    if args[0] in return_value:
        return return_value.get(args[0])
    
class TestPVCliDriver:
    def test_get_config_file(self):
        with mock.patch.dict('picovico.clidriver.os.environ', clear=True) as m:
            with pytest.raises(pv_exceptions.PicovicoCLIError) as e:
                cfg_file = cli.get_config_file()
        with mock.patch('picovico.clidriver.os.makedirs') as m:
            e = OSError("Some Error.")
            e.errno = errno.EIO
            m.side_effect = e
            with pytest.raises(OSError) as e:
                cfg_file = cli.get_config_file()
            assert e.value.errno != errno.EEXIST
            e = OSError("File exists.")
            e.errno = errno.EEXIST
            m.side_effect = e
            cfg_file = cli.get_config_file()
            filename = os.path.join(os.path.join(os.environ['HOME'], '.picovico'), 'profile.ini')
            assert cli.get_config_file() == filename

    def test_necessary_configs(self, profile_fp_default):
        cfg = six.moves.configparser.SafeConfigParser()
        cfg.readfp(profile_fp_default)
        with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            cli.has_necessary_configs(cfg)
        assert exc.value.code == 0
        with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            cli.has_necessary_configs(cfg, 'someother')
        assert exc.value.code == 10
        profile_fp_default.write('DEVICE_ID=device_id\n')
        profile_fp_default.seek(0)
        cfg.readfp(profile_fp_default)
        assert cli.has_necessary_configs(cfg)

    def test_optional_configs(self, profile_fp_default):
        cfg = six.moves.configparser.SafeConfigParser()
        cfg.readfp(profile_fp_default)
        with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            cli.has_optional_secret_configs(cfg)
        assert exc.value.code == 5
        with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            cli.has_optional_username_configs(cfg)
        assert exc.value.code == 5
        with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            cli.has_optional_configs(cfg,both=True)
        assert exc.value.code == 5
        profile_fp_default.write('APP_SECRET=app_secret\n')
        profile_fp_default.seek(0)
        cfg.readfp(profile_fp_default)
        assert cli.has_optional_secret_configs(cfg)
        with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            cli.has_optional_username_configs(cfg)
        assert cli.has_optional_configs(cfg)
        up = ('[DEFAULT]\n', 'ACCESS_KEY=access_key\n', 'ACCESS_TOKEN=access_token\n')
        profile_fp_default.write(up[1])
        profile_fp_default.seek(0)
        cfg.readfp(profile_fp_default)
        with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            cli.has_optional_token_configs(cfg)
        profile_fp_default.write(up[2])
        profile_fp_default.seek(0)
        cfg.readfp(profile_fp_default)
        assert cli.has_optional_token_configs(cfg)
        cfg = six.moves.configparser.SafeConfigParser()
        fp = six.StringIO()
        fp.writelines(up[0]+('USERNAME=username\n'))
        fp.seek(0)
        cfg.readfp(fp)
        with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            cli.has_optional_secret_configs(cfg)
        assert cli.has_optional_configs(cfg)
    
    def test_get_configure_profile(self):
        basic_values = ('APP_ID', 'DEVICE_ID', 'SECTION')
        with mock.patch('picovico.clidriver.six.moves.input') as m:
            m.side_effect = configure_mocked
            profile_info = cli.get_configure_profile()
            assert profile_info.APP_ID == return_args[0]
            assert profile_info.DEVICE_ID == cli.DEFAULT_DEVICE_ID
            assert profile_info.SECTION == cli.DEFAULT_SECTION_NAME
            for attr in profile_info._fields:
                if attr not in basic_values:
                    assert getattr(profile_info, attr) is None
            return_value.update({input_args[1]:'MY_DEVICE_ID'})
            profile_info = cli.get_configure_profile()
            assert profile_info.DEVICE_ID != cli.DEFAULT_DEVICE_ID
            assert profile_info.DEVICE_ID == 'MY_DEVICE_ID'
            profile_info = cli.get_configure_profile('New Profile')
            assert profile_info.SECTION != cli.DEFAULT_SECTION_NAME
            profile_info = cli.get_configure_profile(auth=True)
            assert profile_info.APP_SECRET is not None 
            assert profile_info.APP_SECRET == return_args[2] 
            assert profile_info.USERNAME is None 
            assert profile_info.PASSWORD is None 
            profile_info = cli.get_configure_profile(login=True)
            assert profile_info.APP_SECRET is None 
            assert profile_info.USERNAME is not None 
            assert profile_info.PASSWORD is not None
            profile_info = cli.get_configure_profile(login=True, auth=True)
            assert profile_info.APP_SECRET is None 
            assert profile_info.USERNAME is None 
            assert profile_info.PASSWORD is None 
            assert profile_info.AUTH is None
    
    def test_create_conf_values(self):
        value_to_test = (('MY_ATTR', 'MY_VALUE'),)
        values = cli.create_conf_values(value_to_test)
        for val in values:
            assert val.attr == value_to_test[0][0]    
            assert val.value == value_to_test[0][1]
    
    def test_read_config_values(self, profile_fp_default, profile_fp_other):
        cfg = six.moves.configparser.SafeConfigParser()
        cfg.readfp(profile_fp_default)
        with mock.patch('picovico.clidriver.get_config') as m:
            m.return_value = cfg
            config = cli.read_config_values(cli.DEFAULT_SECTION_NAME)
            assert config.APP_ID == 'default_app_id'
        cfg.readfp(profile_fp_other)
        with mock.patch('picovico.clidriver.get_config') as m:
            m.return_value = cfg
            config = cli.read_config_values('OTHER')
            assert config.APP_ID == 'other_app_id'
        
    def test_set_configs(self, profile_fp_default, profile_fp_other):
        cfg = six.moves.configparser.SafeConfigParser()
        cfg.readfp(profile_fp_default)
        old_cfg = cfg.items(cli.DEFAULT_SECTION_NAME)
        with pytest.raises(six.moves.configparser.NoOptionError):
            cfg.get(cli.DEFAULT_SECTION_NAME, 'DEVICE_ID')
        values = cli.create_conf_values(((a, return_args[i]) for i, a in enumerate(cli.NECESSARY_INFO)))
        with mock.patch('picovico.clidriver.get_config') as m:
            m.return_value = cfg
            cli.set_configs(values)
            assert old_cfg != cfg.items(cli.DEFAULT_SECTION_NAME)
            assert cfg.get(cli.DEFAULT_SECTION_NAME, 'DEVICE_ID')
    
    def test_write_access_info(self):
        profiles = {k: None for k in cli.Profile._fields}
        profiles.update({
            'SECTION': cli.DEFAULT_SECTION_NAME,
            'AUTH': True,
            'APP_ID': 'MY_APP_ID',
            'APP_SECRET': 'MY_APP_SECRET'
        })
        token_returns = ('MY_ACCESS_KEY', 'MY_ACCESS_TOKEN')
        profile = cli.Profile(**profiles)
        patch_login = mock.patch('picovico.PicovicoAPI.login')
        patch_auth = mock.patch('picovico.PicovicoAPI.authenticate')
        patch_tokens = mock.patch('picovico.PicovicoAPI.set_access_tokens')
        patch_key = mock.patch('picovico.PicovicoAPI.access_key', new_callabale=mock.PropertyMock, return_value=token_returns[0])
        patch_token = mock.patch('picovico.PicovicoAPI.access_token', new_callable=mock.PropertyMock, return_value=token_returns[1])
        patch_config = mock.patch('picovico.clidriver.set_configs')
        patch_create_conf = mock.patch('picovico.clidriver.create_conf_values')
        def set_config_side_effect(*args, **kwargs):
            argument = args[0]
            if len(argument) > 1:
                assert all(getattr(a, 'attr') in cli.OPTIONAL_INFO_TOKEN for a in argument)
                #assert all([getattr(a, 'value') in token_returns for a in argument])
                for i, a in enumerate(argument):
                    print a.value
                    if a.attr == cli.OPTIONAL_INFO_TOKEN[i]:
                        pass
                        #assert a.value == token_returns[i]
            else:
                assert argument[0].attr == 'APP_SECRET'
                assert argument[0].value == profile.APP_SECRET
        def create_conf_side_effect(*args, **kwargs):
            print args
        with patch_auth, patch_login, patch_tokens, patch_token, patch_key, patch_create_conf as pcf, patch_config as pc:
            #pc.side_effect = set_config_side_effect
            pcf.side_effect = create_conf_side_effect
            cli.write_access_info(profile)

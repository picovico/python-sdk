import os
import errno

import six
import pytest
import mock

from picovico import exceptions as pv_exceptions
from picovico import clidriver as cli


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

    def test_necessary_configs(self, profile_fp):
        cfg = six.moves.configparser.SafeConfigParser()
        cfg.readfp(profile_fp)
        with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            cli.has_necessary_configs(cfg)
        assert exc.value.code == 0
        with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            cli.has_necessary_configs(cfg, 'someother')
        assert exc.value.code == 10
        profile_fp.write('DEVICE_ID=device_id\n')
        profile_fp.seek(0)
        cfg.readfp(profile_fp)
        assert cli.has_necessary_configs(cfg)

    def test_optional_configs(self, profile_fp):
        cfg = six.moves.configparser.SafeConfigParser()
        cfg.readfp(profile_fp)
        with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            cli.has_optional_secret_configs(cfg)
        assert exc.value.code == 5
        with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            cli.has_optional_username_configs(cfg)
        assert exc.value.code == 5
        with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            cli.has_optional_configs(cfg,both=True)
        assert exc.value.code == 5
        profile_fp.write('APP_SECRET=app_secret\n')
        profile_fp.seek(0)
        cfg.readfp(profile_fp)
        assert cli.has_optional_secret_configs(cfg)
        with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            cli.has_optional_username_configs(cfg)
        assert cli.has_optional_configs(cfg)
        up = ('[default]\n', 'USERNAME=username\n', 'PASSWORD=password\n')
        profile_fp.write(up[1])
        profile_fp.seek(0)
        cfg.readfp(profile_fp)
        with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            cli.has_optional_username_configs(cfg)
        profile_fp.write(up[2])
        profile_fp.seek(0)
        cfg.readfp(profile_fp)
        assert cli.has_optional_username_configs(cfg)
        cfg = six.moves.configparser.SafeConfigParser()
        fp = six.StringIO()
        fp.writelines(up)
        fp.seek(0)
        cfg.readfp(fp)
        with pytest.raises(pv_exceptions.PicovicoProfileError) as exc:
            cli.has_optional_secret_configs(cfg)
        assert cli.has_optional_configs(cfg)

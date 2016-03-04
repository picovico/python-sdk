import os
import errno

import pytest

from picovico.cli import file_utils as pv_cli_file_utility

def file_mock(mocker, return_value=None, side_effect=None, open_data=None):
    mo = mocker.patch('picovico.cli.file_utils.open')
    if return_value:
        mo.return_value = return_value
    if side_effect:
        mo.side_effect = side_effect
    return mo

class TestPVCliFileUtilities:
    def test_get_user_directory_for_storage(self, mocker):
        mocker.patch.dict('picovico.cli.file_utils.os.environ', clear=True)
        with pytest.raises(EnvironmentError):
            cfg_file = pv_cli_file_utility.get_user_directory_for_storage()
        mocker.stopall()
        m = mocker.patch('picovico.cli.file_utils.os.makedirs')
        e = OSError("Some Error.")
        e.errno = errno.EIO
        m.side_effect = e
        with pytest.raises(OSError) as e:
            pv_cli_file_utility.get_user_directory_for_storage()
        assert e.value.errno != errno.EEXIST
        e = OSError("File exists.")
        e.errno = errno.EEXIST
        m.side_effect = e
        pv_config_dir = pv_cli_file_utility.get_user_directory_for_storage()
        pv_actual_config_dir = os.path.join(os.environ['HOME'], '.picovico')
        assert pv_config_dir == pv_actual_config_dir
    
    def test_get_file_functions(self, mocker):
        pv_config_dir = os.path.join(os.environ['HOME'], '.picovico')
        m = mocker.patch('picovico.cli.file_utils.get_user_directory_for_storage')
        m.return_value = pv_config_dir
        profile_file = pv_cli_file_utility.get_file_from_storage('profile.ini')
        assert profile_file == os.path.join(pv_config_dir, 'profile.ini')
        assert profile_file == pv_cli_file_utility.get_profile_file()
        session_file = pv_cli_file_utility.get_file_from_storage('session')
        assert profile_file != session_file
        assert session_file == os.path.join(pv_config_dir, 'session')
        assert session_file == pv_cli_file_utility.get_session_file()
        project_file = pv_cli_file_utility.get_file_from_storage('project')
        assert project_file != session_file != profile_file
        assert project_file == os.path.join(pv_config_dir, 'project')
        assert project_file == pv_cli_file_utility.get_project_file()
    
    def test_file_obj(self, mocker):
        e = IOError()
        e.errno = errno.EPERM
        def side_effect(*args, **kwargs):
            if args[0] == 'nofile':
                raise e
        file_mock(mocker, side_effect=side_effect)
        with pytest.raises(IOError):
            pv_cli_file_utility.get_file_obj('nofile')
        e.errno = errno.ENOENT
        pv_cli_file_utility.get_file_obj('nofile')

import os
import errno

import pytest

from picovico.cli import file_utils as pv_cli_file_utility

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
            cfg_file = pv_cli_file_utility.get_user_directory_for_storage()
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
        assert session_file == pv_cli_file_utility.get_session_file()
    
    #def test_session_read_and_saves(self, mocker):
        #session_file = os.path.join(os.path.join(os.environ['HOME'], '.picovico'), 'session')
        #m = mocker.patch('picovico.cli.file_utils.get_session_file')
        #m.return_value = session_file
        #mocker.patch('picovico.cli.file_utils.open')
        #json_mock = mocker.patch('picovico.cli.file_utils.json.load')
        

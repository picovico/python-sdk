import itertools
import pytest

from picovico import PicovicoAPI
from picovico.cli import project_driver as pv_project_driver

class TestProjectDriver:
    @pytest.mark.parametrize('video_id,video_data', itertools.product((None, 'vid'), (None, {'vid': True})))
    def test_get_project_api(self, mocker, video_id, video_data):
        mapi = mocker.Mock(spec=PicovicoAPI)
        mapi.project = mocker.Mock(return_value='Project')
        mocker.patch('picovico.cli.project_driver.pv_utility.prepare_api_object', return_value=mapi)
        mocker.patch('picovico.cli.project_driver.file_utils.read_from_project_file', return_value=video_data)
        mpv = mocker.patch('picovico.cli.project_driver.populate_vdd_to_project')
        pv_project_driver.get_project_api('Hello', video=video_id)
        if not video_id and not video_data:
            mpv.assert_not_called()
        else:
            if video_data:
                mpv.assert_called_with(mapi.project, True)
        
    
    

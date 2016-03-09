import itertools
import pytest

from picovico import PicovicoAPI
from picovico.cli import project_driver as pv_project_driver
from picovico import project as pv_project

class TestProjectDriver:
    @pytest.mark.parametrize('video_id,video_data', itertools.product((None, 'vid'), (None, {'vid': True})))
    def test_get_project_api(self, mocker, video_id, video_data):
        mapi = mocker.Mock(spec=PicovicoAPI)
        mapi.project = mocker.Mock(return_value='Project')
        mocker.patch('picovico.cli.project_driver.pv_utility.prepare_api_object', return_value=mapi)
        mocker.patch('picovico.cli.project_driver.file_utils.read_from_project_file', return_value=video_data)
        mpv = mocker.patch('picovico.cli.project_driver.populate_vdd_to_project')
        pv_project_driver.get_project_api('Hello', video=video_id)
        if not video_data:
            mpv.assert_not_called()
        else:
            mpv.assert_called_with(mapi.project, True)
        
    
    def test_prepare_text_method_args(self):
        with pytest.raises(AssertionError):
            pv_project_driver.prepare_text_method_args()
        tb = pv_project_driver.prepare_text_method_args(title='Hello')
        assert tb.METHOD == 'add_text'    
        assert tb.ARGUMENTS and tb.ARGUMENTS['title'] == 'Hello' 
        assert not all(tb.ARGUMENTS.values())
        tb = pv_project_driver.prepare_text_method_args(title='Hello', body='There')
        assert all(tb.ARGUMENTS.values())
        
    @pytest.mark.parametrize('keyarg', ({'id': 'some_id'}, {'filename': 'some_file'}, {'url': 'some_url'}))
    def test_prepare_photo_music_method_args(self, keyarg):
        pma = pv_project_driver.prepare_photo_method_args(**keyarg)
        meth_name = 'add_photo'
        if 'url' in keyarg or 'filename' in keyarg:
            meth_name = 'add_photo_url' if 'url' in keyarg else 'add_photo_file'
        assert pma.METHOD == meth_name
        keyarg.update(caption='caption')
        pma = pv_project_driver.prepare_photo_method_args(**keyarg)
        assert pma.ARGUMENTS['caption'] == 'caption'
        if 'id' in keyarg:
            keyarg.update(url='some_url')
            with pytest.raises(AssertionError):
                pv_project_driver._prepare_common_args(**keyarg)

    @pytest.mark.parametrize('comp', pv_project.Vdd._fields)
    def test_prepare_common_method_with_args(self, comp):
        assert not pv_project_driver.prepare_common_methods_with_args()
        arg = {comp: '{}_value'.format(comp)}
        tpc = pv_project_driver.prepare_common_methods_with_args(**arg)
        if comp in ('assets', 'credits'):
            assert not tpc
        

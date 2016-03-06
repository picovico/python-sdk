import collections

import six
import pytest

from picovico import project as pv_project
from picovico import exceptions as pv_exceptions
from picovico import constants as pv_constants

class TestProject:
    def test_project_initiation_and_property(self, pv_request):
        with pytest.raises(pv_exceptions.PicovicoProjectNotAllowed):
            pv_project.PicovicoProject(pv_request.NOAUTH)
        project = pv_project.PicovicoProject(pv_request.AUTH)
        assert not project.video
        assert project.vdd.name == pv_constants.VIDEO_NAME
        assert project.vdd.quality in pv_constants.QUALITY
        assert project.vdd.style is None
        assert not project.vdd.assets
    
    def test_set_name_style_quality(self, pv_request):
        project = pv_project.PicovicoProject(pv_request.AUTH)
        assert project.vdd.name == pv_constants.VIDEO_NAME
        project.set_name('New Video')
        assert project.vdd.name == 'New Video'
    
    #def test_project_begin_decorator(self, pv_request):
        #project = pv_project.PicovicoProject(pv_request.AUTH)
        #with pytest.raises(pv_exceptions.PicovicoProjectNotAllowed):
            #project.set_style('My New Style')
    
    def test_set_style_quality(self, pv_request, pv_mocks):
        mocker = pv_mocks.OBJ
        mocker.patch.object(pv_project.PicovicoProject, 'video')
        project = pv_project.PicovicoProject(pv_request.AUTH)
        assert project.vdd.style != 'My Style'
        project.set_style('My Style')
        assert project.vdd.style == 'My Style'
        with pytest.raises(AssertionError):
            project.set_quality(40)
        project.set_quality(pv_constants.QUALITY.MEDIUM)
        assert project.vdd.quality == pv_constants.QUALITY.MEDIUM
        
    
    def test_assets_functionality(self, pv_request, pv_mocks):
        mocker = pv_mocks.OBJ
        mocker.patch.object(pv_project.PicovicoProject, 'video')
        project = pv_project.PicovicoProject(pv_request.AUTH)
        assert not project.vdd.assets
        project.add_text(title='Hello', body='Just a Test')
        assert project.vdd.assets
        project.add_text('Second')
        project.add_music('music_id')
        project.add_photo('photo_id')
        project.add_photo('photo_id_caption', caption='With Caption')
        assert len(project.vdd.assets) == 5
        assert any(d['asset'] == 'music' for d in project.vdd.assets)
        vdd = project.populate_vdd()
        assert isinstance(vdd['assets'], six.string_types)  
        project.clear_assets()
        assert not project.vdd.assets  

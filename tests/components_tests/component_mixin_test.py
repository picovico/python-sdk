import pytest
from picovico.components import *
from picovico.components import PicovicoComponentMixin
from picovico import baserequest as pv_base
from picovico import exceptions as pv_exceptions

class TestComponentMixin:
    def test_component_property(self):
        pv_component = PicovicoComponentMixin()
        with pytest.raises(AttributeError):
            pv_component.music_component
        with pytest.raises(AttributeError):
            pv_component.other_component
        pv_component._ready_component_property()
        assert pv_component.photo_component


class TestComponent:
    #def test_component_methods(self):
        #components = {k: None for k in ('music', 'photo', 'style', 'video')}
        #classes = (PicovicoMusic, PicovicoPhoto, PicovicoStyle, PicovicoVideo)
        #component_class = dict(zip(('music', 'photo', 'style', 'video'), classes))
        #for name in components:
            #components[name] = component_class[name](pv_base.PicovicoRequest())
        #music_component = components.get('music')
        #style_component = components.get('style')
        #video_component = components.get('video')
        #photo_component = components.get('photo')

    def test_photo_component(self):
        pv_comp = PicovicoPhoto(pv_base.PicovicoRequest())
        with pytest.raises(pv_exceptions.PicovicoAPINotAllowed):
            gm = pv_comp.all()

    def test_style_component(self):
        pv_comp = PicovicoStyle(pv_base.PicovicoRequest())
        with pytest.raises(NotImplementedError):
            pv_comp.upload_file(1)
        with pytest.raises(NotImplementedError):
            pv_comp.delete(1)

    def test_library_and_free_component(self, mock_obj, response, method_calls, headers, pv_urls):
        request_mock = mock_obj.REQUEST
        req = pv_base.PicovicoRequest(headers.AUTH)
        style_component = PicovicoStyle(req)
        request_mock.return_value = response.SUCCESS.OK
        get_call = method_calls.GET_AUTH.copy()
        get_call.update(url=pv_urls.MY_STYLES)
        style_component.get_library()
        request_mock.assert_called_with(**get_call)
        style_component.get_free()
        get_call.pop('headers')
        get_call.update(url=pv_urls.PICOVICO_STYLES)
        request_mock.assert_called_with(**get_call)

import pytest
from picovico.components import PicovicoComponentMixin


class TestComponentMixin:
    def test_component_property(self):
        pv_component = PicovicoComponentMixin()
        with pytest.raises(AttributeError):
            pv_component.music_component
        with pytest.raises(AttributeError):
            pv_component.other_component
        pv_component._ready_component_property()
        assert pv_component.photo_component

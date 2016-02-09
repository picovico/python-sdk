import abc

import six

from .base import PicovicoBaseComponent
from .video import PicovicoVideo
from .style import PicovicoStyle
from .music import PicovicoMusic
from .photo import PicovicoPhoto

from .. import baserequest as pv_base


class PicovicoComponentMixin(object):
    """ Picovico mixin for components.(Abstract)
    This is just a mixin. Shouldn't be used alone.
    """
    __metaclass__ = abc.ABCMeta
    def __init__(self):
        self._pv_request = pv_base.PicovicoRequest()
        #def get_specific_library(name):
            #pv_comp_base = PicovicoBaseComponent(self._pv_request, name)
            #return getattr(pv_comp_base, 'get_library_{}s'.format(name))
        #for k in PicovicoBaseComponent._components[:2]:
            #setattr(self, 'get_library_{}s'.format(k), get_specific_library(k))
        
    def _ready_component_property(self):
        self.__components = {}
        def get_func_from_name(name):
            def property_func(self):
                return self.__components[name]
            return property_func
        classes = (PicovicoStyle, PicovicoMusic, PicovicoPhoto, PicovicoVideo)
        component_class = dict(six.moves.zip(PicovicoBaseComponent._components, classes))
        for k in PicovicoBaseComponent._components:
            self.__components[k] = component_class[k](self._pv_request)
            setattr(PicovicoComponentMixin, '{}_component'.format(k), property(get_func_from_name(k)))


__all__ = ['PicovicoVideo', 'PicovicoMusic', 'PicovicoStyle', 'PicovicoPhoto']

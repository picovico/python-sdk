import abc
import collections

import six

from .base import PicovicoBaseComponent
from .video import PicovicoVideo
from .style import PicovicoStyle
from .music import PicovicoMusic
from .photo import PicovicoPhoto

from .. import urls as pv_urls
from .. import baserequest as pv_base

class PicovicoComponentMixin(object):
    """ Picovico-SDK: Mixin class for component.

    This is a mixin class inherited by API class.
    """

    __metaclass__ = abc.ABCMeta

    def __get_free(self, component):
        url = getattr(pv_urls, 'PICOVICO_{}S'.format(component))
        if self._pv_request.is_authenticated():
            free_req = pv_base.PicovicoRequest()
        else:
            free_req = self._pv_request
        def req():
            return free_req.get(url)
        return req

    def __init__(self):
        super(PicovicoComponentMixin, self).__init__()
        self._pv_request = pv_base.PicovicoRequest()
        for component in ('music', 'style'):
            setattr(self, 'free_{}s'.format(component), self.__get_free(component.upper())) 
            #self._ready_component_property()

    def _ready_component_property(self):
        """ **Not for user.
        Readies read-only component properties.
        """
        self.__components = None
        Components = collections.namedtuple('Component', PicovicoBaseComponent._components)
        def get_func_from_name(name):
            def property_func(self):
                return getattr(self.__components, name, None)
            return property_func
        classes = (PicovicoStyle, PicovicoMusic, PicovicoPhoto, PicovicoVideo)
        component_class = dict(six.moves.zip(PicovicoBaseComponent._components, classes))
        for k in PicovicoBaseComponent._components:
            component_class[k] = component_class[k](self._pv_request)
            setattr(PicovicoComponentMixin, '{}_component'.format(k), property(get_func_from_name(k)))
        self.__components= Components(**component_class)


# allow only specific components when * imported.
__all__ = ['PicovicoVideo', 'PicovicoMusic', 'PicovicoStyle', 'PicovicoPhoto']

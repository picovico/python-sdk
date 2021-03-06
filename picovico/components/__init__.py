import abc
import collections

import six

from picovico.components.base import PicovicoBaseComponent
from picovico.components.video import PicovicoVideo
from picovico.components.style import PicovicoStyle
from picovico.components.music import PicovicoMusic
from picovico.components.photo import PicovicoPhoto

from picovico import urls as pv_urls
from picovico import baserequest as pv_request

# _doc_map = {
    # 'video': PicovicoVideo,
    # 'music': PicovicoMusic,
    # 'style': PicovicoStyle,
    # 'photo': PicovicoPhoto,
# }
# for k, v in _doc_map.items():
    # for meth in ('one', 'all', 'delete', 'get_free', 'upload_file'):
        # doc = getattr(v, meth)
        # setattr(doc.__func__, '__doc__', doc.__doc__.format(k))

class PicovicoComponentMixin(object):
    """ Picovico-SDK: Mixin class for component.

    This is a mixin class inherited by API class.
    """

    __metaclass__ = abc.ABCMeta

    def __get_free(self, component):
        url = getattr(pv_urls, 'PICOVICO_{}S'.format(component))
        if self._pv_request.is_authenticated():
            free_req = pv_request.PicovicoRequest()
        else:
            free_req = self._pv_request
        def req():
            return free_req.get(url)
        return req

    def __init__(self):
        super(PicovicoComponentMixin, self).__init__()
        self._pv_request = pv_request.PicovicoRequest()
        for component in ('music', 'style'):
            setattr(self, 'free_{}s'.format(component), self.__get_free(component.upper())) 
            # doc = 'Picovico offered {}s'.format(component)
            # func = getattr(PicovicoComponentMixin, 'free_{}s'.format(component))
            # func.__func__.__doc__ = doc
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

from . import exceptions as pv_exceptions
from . import components as pv_components
from . import constants as pv_constants

class PicovicoProject(object):
    
    __quality = pv_constants.QUALITY.STANDARD
    
    def __init__(self, request_obj):
        self.photo_component = pv_components.PicovicoPhoto(request_obj)
        self.video_component = pv_components.PicovicoVideo(request_obj)
        self.music_component = pv_components.PicovicoMusic(request_obj)
        self.style_component = pv_components.PicovicoStyle(request_obj)
    
    def __api_call(self, **kwargs):
        assert all(k in kwargs for k in ('method', 'url'))
        method = kwargs.pop('method')
        return getattr(self._pv_request, method)(**kwargs)
    
    @property
    def video(self):
        return self.__video
    
    @property
    def style(self):
        return self.__style
        
    @style.setter
    def style(self, value):
        assert value, 'Style name is required.'
        #if value:
            #style = self.style_component.get(value)
        self.__style = value
        
    
    @property
    def name(self):
        return self.__name


    @name.setter
    def name(self, val):
        val = val or 'Untitled Video'
        self.__name = val
        
    
    @property
    def quality(self):
        return self.__quality
        
    
    @quality.setter
    def quality(self, val):
        assert val in pv_constants.QUALITY, '{} is not supported.'.format(val)
        self.__quality = val
        
    
    @property
    def assets(self):
        pass
        
    
    def begin(self, name=None):
        if name is not None:
            self.name = name
        res = self.video_component.new(self.name)
        self.__video = res['video_id']

    def discard(self):
        pass
    
    def save(self):
        pass
    
    def render(self):
        pass
    
    def preview(self):
        pass

    def add_assets(self, **kwargs):
        pass

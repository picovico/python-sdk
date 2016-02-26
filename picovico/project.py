import collections

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
        self.__vdd = {'assets': []}

    # def __api_call(self, **kwargs):
        # assert all(k in kwargs for k in ('method', 'url'))
        # method = kwargs.pop('method')
        # return getattr(self._pv_request, method)(**kwargs)

    # @property
    # def vdd(self):
        # return self.__vdd

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
        return self.__vdd['assets']

    def begin(self, name=None):
        if name is not None:
            self.name = name
        res = self.video_component.new(self.name)
        self.__video = res['id']

    def discard(self):
        self.video_component.delete(self.video)

    def save(self):
        self.video_component.save()

    def render(self):
        self.video_component.render(self.video)

    def preview(self):
        self.video_component.preview(self.video)

    @staticmethod
    def time_counter(vdd):
        start = len(vdd['assets'])
        return {
            'start_time': start,
            'end_time': start+5
        }

    @staticmethod
    def create_asset_dict(asset_type, asset_id=None, data=None):
        asset_dict = {
            'asset': asset_type,
        }
        if asset_id:
            asset_dict.update(asset_id=asset_id)
        if data:
            asset_dict.update(data=data)
        return asset_dict

    #def __create_music_asset(self, music_id):
        #self.

    @pv_decorator.pv_project_check_begin
    def add_music(self, music_id):
        """ Picovico: If user already knows the music id. """
        music_asset = self.create_asset_dict('music', music_id)
        self._vdd['assets'].append(music_asset)

    @pv_decorator.pv_project_check_begin
    def add_text(self, title=None, text=None):
        text_data = {
            'title': title,
            'text': text
        }
        text_asset = self.create_asset_dict('text', data=text_data)
        text_asset.update(self.time_counter(self.vdd))
        self.__vdd['assets'].append(text_asset)

    @pv_decorator.pv_project_check_begin
    def add_photo(self, photo_id, caption=None)
        photo_data = {'caption': caption} if caption else None
        photo_asset = self.create_asset_dict('photo', photo_id, photo_data)
        photo_asset.update(self.time_counter(self.vdd))
        self._vdd['assets'].append(photo_asset)

    @pv_decorator.pv_project_check_begin
    def __component_actions(self, component, method_name, **kwargs):
        component_method = getattr(getattr(self, '{}_component'.format(component)), method_name)
        return component_method(**kwargs)

    def add_music_url(self, url, preview=None):
        res = self.__component_actions('music', 'upload_url', url=url, preview=preview)
        self.add_music(res['id'])

    def add_music_file(self, filename):
        res = self.__component_actions('music', 'upload_file', filename=filename)
        self.add_music(res['id'])

    def add_photo_url(self, url, thumbnail=None, caption=None):
        res = self.__component_actions('photo', 'upload_url', url=url, thumbnail=thumbnail)
        self.add_photo(res['id'], caption)

    def add_photo_file(self, filename, caption=None):
        res = self.__component_actions('photo', 'upload_file', filename=filename)
        self.add_photo(res['id'], caption)


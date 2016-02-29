import json
import collections

from . import exceptions as pv_exceptions
from . import components as pv_components
from . import constants as pv_constants
from . import decorators as pv_decorator

class PicovicoProject(object):

    # __quality = pv_constants.QUALITY.STANDARD

    def __init__(self, request_obj):
        self.photo_component = pv_components.PicovicoPhoto(request_obj)
        self.video_component = pv_components.PicovicoVideo(request_obj)
        self.music_component = pv_components.PicovicoMusic(request_obj)
        self.style_component = pv_components.PicovicoStyle(request_obj)
        Vdd = collections.namedtuple('VideoDefinitionData', ('assets', 'style', 'name', 'quality'))
        self.__vdd = Vdd([], None, pv_constants.VIDEO_NAME, pv_constants.QUALITY.STANDARD)

    # def __api_call(self, **kwargs):
        # assert all(k in kwargs for k in ('method', 'url'))
        # method = kwargs.pop('method')
        # return getattr(self._pv_request, method)(**kwargs)

    @property
    def vdd(self):
        return self.__vdd

    @property
    def video(self):
        return self.__video

    # @property
    # def style(self):
        # return self.__style

    # @style.setter
    # def style(self, value):
        # assert value, 'Style name is required.'
        # #if value:
            # #style = self.style_component.get(value)
        # self.__style = value


    # @property
    # def name(self):
        # return self.__name


    # @name.setter
    # def name(self, val):
        # val = val or 'Untitled Video'
        # self.__name = val


    # @property
    # def quality(self):
        # return self.__quality


    # @quality.setter
    # def quality(self, val):
        # assert val in pv_constants.QUALITY, '{} is not supported.'.format(val)
        # self.__quality = val


    # @property
    # def assets(self):
        # return self.__assets

    # @assets.setter
    # def assets(self, val):
        # assert isinstance(val, dict)
        # self.__assets.append(val)

    def begin(self, name=None):
        self.add_name(name)
        res = self.video_component.new(self.vdd.name)
        self.__video = res['id']

    def discard(self):
        self.video_component.delete(self.video)

    def save(self):
        vdd = self.populate_vdd()
        if vdd:
            self.video_component.save(self.video, vdd)

    def render(self):
        self.video_component.render(self.video)

    def preview(self):
        self.video_component.preview(self.video)

    def populate_vdd(self):
        vdd = {}
        vdd.update(name=self.vdd.name)
        vdd.update(style=self.vdd.style)
        vdd.update(quality=self.vdd.quality)
        vdd.update(assets=json.dumps(self.vdd.assets))
        return vdd
        # self._vdd.update(assets=json.dumps(self.assets))

    @staticmethod
    def time_counter(assets):
        start = len(assets)
        return {
            'start_time': start,
            'end_time': start+5
        }


    @staticmethod
    def create_asset_dict(asset_type, asset_id=None, data=None):
        asset_dict = {
            'asset': asset_type,
            'start_time': 0,
            'end_time': 0
        }
        if asset_id:
            asset_dict.update(asset_id=asset_id)
        if data:
            asset_dict.update(data=data)
        # AssetClass = collections.namedtuple('{}Asset'.format('asset_type'), asset_dict.keys())
        return asset_dict

    def __add_asset(self, asset, time=False):
        if time:
            asset.update(self.time_counter(self.vdd.assets))
        self.vdd.assets.append(asset)
        
    @pv_decorator.pv_project_check_begin
    def add_style(self, style_name):
        assert style_name, 'Empty Style not allowed.'
        self.vdd._replace(style=style_name)
        
    @pv_decorator.pv_project_check_begin
    def add_quality(self, val):
        assert val in pv_constants.QUALITY, '{} is not supported.'.format(val)
        self.vdd._replace(quality=val)
        
    def add_name(self, val):
        self.vdd._replace(name=val or pv_constants.VIDEO_NAME)
    #def __create_music_asset(self, music_id):
        #self.

    @pv_decorator.pv_project_check_begin
    def add_music(self, music_id):
        """ Picovico: If user already knows the music id. """
        music_asset = self.create_asset_dict('music', music_id)
        self.__add_asset(music_asset)

    @pv_decorator.pv_project_check_begin
    def add_text(self, title=None, text=None):
        text_data = {
            'title': title,
            'text': text
        }
        text_asset = self.create_asset_dict('text', data=text_data)
        self.__add_asset(text_asset)

    @pv_decorator.pv_project_check_begin
    def add_photo(self, photo_id, caption=None):
        photo_data = {'caption': caption} if caption else None
        photo_asset = self.create_asset_dict('photo', photo_id, photo_data)
        self.__add_asset(photo_asset)

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
    
    @pv_decorator.pv_project_check_begin
    def clear_assets(self):
        self.vdd.assets = []
    #def remove_asset(self, asset_type, asset_id, title):
        #assets = self.vdd.assets
        #for asset in assets:
            #id = asset.get('asset_id', None)
            #_type = asset.get('asset_type')
            #_title = asset.get('data').get('title', None)
            #if asset_type == _type and (_title == title or id == asset_id):
                 


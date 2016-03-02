import json
import collections

from . import exceptions as pv_exceptions
from . import components as pv_components
from . import constants as pv_constants
from . import decorators as pv_decorator

Vdd = collections.namedtuple('VideoDefinitionData', ('name', 'style', 'quality', 'assets', 'privacy', 'credits'))

class PicovicoProject(object):
    def __init__(self, request_obj):
        if not request_obj.is_authenticated():
            raise pv_exceptions.PicovicoProjectNotAllowed('You cannot initiate project without authenticating.')
        self.photo_component = pv_components.PicovicoPhoto(request_obj)
        self.video_component = pv_components.PicovicoVideo(request_obj)
        self.music_component = pv_components.PicovicoMusic(request_obj)
        self.style_component = pv_components.PicovicoStyle(request_obj)
        self.__vdd = Vdd(pv_constants.VIDEO_NAME, None, pv_constants.QUALITY.STANDARD, None, pv_constants.PRIVACY.PRIVATE, None)
        self.__video = None

    @property
    def vdd(self):
        return self.__vdd

    @property
    def video(self):
        return self.__video
    
    @video.setter
    def video(self, id):
        self.__video = id


    def begin(self, name=None):
        self.set_name(name)
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
        vdd.update(privacy=self.vdd.privacy)
        if self.vdd.credits:
            vdd.update(credit=json.dumps(self.vdd.credits))
        return vdd

    @staticmethod
    def time_counter(assets):
        start = 0 if not assets else len(assets)*5
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
        return asset_dict
    
    def _add_assets(self, assets):
        """ Picovico: Not recommended for users but can be used to populate whole assets """
        assert isinstance(assets, list), 'assets should be list'
        self.__replace_vdd_data(assets=assets)

    def _add_credits(self, credits):
        """ Picovico: Not recommended for users but can be used to populate whole assets """
        assert isinstance(credits, list), 'assets should be list'
        self.__replace_vdd_data(credits=credits)
    
    def __add_asset(self, asset, time=True):
        if time:
            asset.update(self.time_counter(self.vdd.assets))
        if self.vdd.assets is None:
            self.__replace_vdd_data(assets=[])
        self.vdd.assets.append(asset)
        
    def __replace_vdd_data(self, **kwargs):
        self.__vdd = self.vdd._replace(**kwargs)

    @pv_decorator.pv_project_check_begin
    def set_style(self, value):
        assert value, 'Empty Style not allowed.'
        self.__replace_vdd_data(style=value)
        
    @pv_decorator.pv_project_check_begin
    def set_quality(self, value):
        assert value in pv_constants.QUALITY, '{0} is not supported. Choose [{1}]'.format(value, ','.join(str(q) for q in pv_constants.QUALITY))
        self.__replace_vdd_data(quality=value)
    
    def set_name(self, value):
        if value:
            self.__replace_vdd_data(name=value)

    @pv_decorator.pv_project_check_begin
    def add_music(self, music_id):
        """ Picovico: If user already knows the music id. """
        music_asset = self.create_asset_dict('music', music_id)
        self.__add_asset(music_asset, time=False)

    @pv_decorator.pv_project_check_begin
    def set_privacy(self, value):
        assert value in pv_constants.PRIVACY, 'Privacy can be [{}]'.format(','.join(pv_constants.PRIVACY))
        self.__replace_vdd_data(privacy=value)
        
    @pv_decorator.pv_project_check_begin
    def add_credit(self, name, value):
        assert all((name, value)), 'Credit should be two texts'
        if self.vdd.credits is None:
            self.__replace_vdd_data(credits=[])
        self.vdd.credits.append((name, value))
        
    @pv_decorator.pv_project_check_begin
    def add_text(self, title=None, body=None):
        assert any((title, body)), 'Title or Text is required'
        text_data = {
            'title': title,
            'text': body
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
        self.__replace_vdd_data(assets=None)

    @pv_decorator.pv_project_check_begin
    def clear_credits(self):
        self.__replace_vdd_data(credits=None)

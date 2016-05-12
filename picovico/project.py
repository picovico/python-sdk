import json
import collections

from picovico import exceptions as pv_exceptions
from picovico import components as pv_components
from picovico import constants as pv_constants
from picovico import decorators as pv_decorators

#: Video Data Definition to be used in project
#: All video related components are stored in `Vdd`
Vdd = collections.namedtuple('VideoDefinitionData', ('name', 'style', 'quality', 'assets', 'privacy', 'credits'))

class PicovicoProject(object):
    """ Picovico-SDK: Project class.

    This class is a helper for stateful video creation process.
    The object will hold all component related actions as well.

    Attributes:
        photo_component: :class:`.PicovicoPhoto` instance.
        video_component: :class:`.PicovicoVideo` instance.
        music_component: :class:`.PicovicoMusic` instance.
        style_component: :class:`.PicovicoStyle` instance.

    Args:
        request_obj(PicovicoRequest): Request object with authentication

    Raises:
        PicovicoProjectNotAllowed: when `request_obj` is not authorized.
    """

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
        """ Read-only :class:`Vdd` instance.
        """
        return self.__vdd

    @property
    def video(self):
        """ Read-only video identifier from project initiation.
        """
        return self.__video

    @video.setter
    def video(self, id):
        self.__video = id


    def begin(self, name=None):
        """ Initiate the video proect.

        Args:
            name(str): *Optional* Name of video or default 'Untitled' name
        """
        self.set_name(name)
        res = self.video_component.new(self.vdd.name)
        self.__video = res['id']

    def discard(self):
        """ Discard current project if set.
        """
        self.video_component.delete(self.video)

    def save(self):
        """ Save `Vdd` component.
        """
        if self.vdd:
            self.video_component.save(self.video, self.populate_vdd())

    def render(self):
        """ Render/Create the video.
        """
        self.video_component.create(self.video)

    def preview(self):
        """ Preview the video.
        """
        self.video_component.preview(self.video)

    def populate_vdd(self):
        """ Make `Vdd` post data.

        Returns:
            dict: data based on :class:`Vdd` instance.
        """
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
        """ Time counter.
        Appends time in assets.
        
        Returns:
            dict: data with 'start_time' and 'end_time'.
        """
        start = 0 if not assets else len(assets)*5
        return {
            'start_time': start,
            'end_time': start+5
        }


    @staticmethod
    def create_asset_dict(asset_type, asset_id=None, data=None):
        """ Asset data creator.
        Creates asset post data from asset type.

        Args:
            asset_type(str): name of asset to be sent.
            asset_id(str): *Optional* id of some asset component
            data(dict): *Optional* additional data to be sent.

        Returns:
            dict: Single Asset post data.
        """
        asset_dict = {
            'name': asset_type,
            'start_time': 0,
            'end_time': 0
        }
        if asset_id:
            asset_dict.update(asset_id=asset_id)
        if data:
            asset_dict.update(data=data)
        return asset_dict

    def _add_assets(self, assets):
        """ **Not for User.
        A helper to populate the whole assets in vdd.

        Args:
            assets(list): list of assets

        Raises:
            AssertionError
        """
        assert isinstance(assets, list), 'assets should be list'
        self.__replace_vdd_data(assets=assets)

    def _add_credits(self, credits):
        """ **Not for User.
        A helper to add whole credits in vdd.

        Args:
            credits(list): list of credits.

        Raises:
            AssertionError
        """
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

    @pv_decorators.pv_project_check_begin
    def set_style(self, value):
        """ Add style to video project.
        Sets :class:`Vdd` style.

        Args:
            value(str): style name of picovico.

        Raises:
            AssertionError
        """
        assert value, 'Empty Style not allowed.'
        self.__replace_vdd_data(style=value)

    @pv_decorators.pv_project_check_begin
    def set_quality(self, value):
        """ Add quality to video project.
        Sets :class:`Vdd` quality.

        Args:
            value(int): allowed quality by picovico

        Raises:
            AssertionError
        """
        assert int(value) in pv_constants.QUALITY, '{0} is not supported. Choose [{1}]'.format(value, ','.join(str(q) for q in pv_constants.QUALITY))
        self.__replace_vdd_data(quality=int(value))

    def set_name(self, value):
        """ Add name to video project.
        Sets :class:`Vdd` name.

        Args:
            value(str): name to set.
        """
        if value:
            self.__replace_vdd_data(name=value)

    @pv_decorators.pv_project_check_begin
    def add_music(self, music_id):
        """ Add music to video project.
        Adds music asset to :class:`Vdd`.

        Args:
            music_id(str): music identifier from picovico.
        """
        music_asset = self.create_asset_dict('music', music_id)
        self.__add_asset(music_asset, time=False)

    @pv_decorators.pv_project_check_begin
    def set_privacy(self, value):
        """ Set privacy of video project.

        Args:
            value(str): value of allowed privacy.
        """
        assert value in pv_constants.PRIVACY, 'Privacy can be [{}]'.format(','.join(pv_constants.PRIVACY))
        self.__replace_vdd_data(privacy=value)

    @pv_decorators.pv_project_check_begin
    def add_credit(self, name, value):
        """ Add single credit to video project.
        Credits are list of length 2.

        Args:
            name(str): first credit value
            value(str): second credit value
        """
        assert all((name, value)), 'Credit should be two texts'
        if self.vdd.credits is None:
            self.__replace_vdd_data(credits=[])
        self.vdd.credits.append((name, value))

    @pv_decorators.pv_project_check_begin
    def add_text(self, title=None, body=None):
        """ Add text asset to video project.

        Args:
            title(str): title of text asset
            body(str): body of text asset that coheres with title

        Raises:
            AssertionError
        """
        assert any((title, body)), 'Title or Text is required'
        text_data = {
            'title': title,
            'text': body
        }
        text_asset = self.create_asset_dict('text', data=text_data)
        self.__add_asset(text_asset)

    @pv_decorators.pv_project_check_begin
    def add_photo(self, photo_id, caption=None):
        """ Add photo asset to video project.

        Args:
            photo_id(str): photo identifier from picovico
            caption(str): caption to be used with photo.
        """
        photo_data = {'caption': caption} if caption else None
        photo_asset = self.create_asset_dict('image', photo_id, photo_data)
        self.__add_asset(photo_asset)

    @pv_decorators.pv_project_check_begin
    def __component_actions(self, component, method_name, **kwargs):
        component_method = getattr(getattr(self, '{}_component'.format(component)), method_name)
        return component_method(**kwargs)

    def add_music_url(self, url, preview=None):
        """ Set music from URL and preview.
        Calls upload url then sets identifier as music asset.

        Args:
            url(str): URL of music
            preview(optional[str]): Preview URL of music.
        """
        res = self.__component_actions('music', 'upload_url', url=url, preview=preview)
        self.add_music(res['id'])

    def add_music_file(self, filename):
        """ Set music from file.
        Calls upload file and then sets identifier in music asset.

        Args:
            filename(str): filname path.
        """
        res = self.__component_actions('music', 'upload_file', filename=filename)
        self.add_music(res['id'])

    def add_photo_url(self, url, thumbnail=None, caption=None):
        """ Set photo asset from url.
        Calls upload_url and then sets identifier in photo asset.

        Args:
            url(str): URL of photo to upload.
            thumbnail(optional[str]): thumbnail URL of photo.
            caption(optional[str]): caption to be used in photo.
        """
        res = self.__component_actions('photo', 'upload_url', url=url, thumbnail=thumbnail)
        self.add_photo(res['id'], caption)

    def add_photo_file(self, filename, caption=None):
        """ Set photo asset from file.
        Calls upload file and then sets identifier in photo asset.

        Args:
            filename(str): path of file.
            caption(optional[str]): caption to be used in photo.
        """
        res = self.__component_actions('photo', 'upload_file', filename=filename)
        self.add_photo(res['id'], caption)

    @pv_decorators.pv_project_check_begin
    def clear_assets(self):
        """ Clear video project vdd assets.
        """
        self.__replace_vdd_data(assets=None)

    @pv_decorators.pv_project_check_begin
    def clear_credits(self):
        """ Clear video project credit assets.
        """
        self.__replace_vdd_data(credits=None)

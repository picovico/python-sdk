from .session import PicovicoSessionMixin
from .components import PicovicoComponentMixin
from .decorators import pv_auth_required
from . import urls as pv_urls
from . import project as pv_project


class PicovicoAPI(PicovicoSessionMixin, PicovicoComponentMixin):
    """ Picovico-SDK: The API class.
    Base class for API activity. It will ready component and project objects based
    on authorization.

    Attributes:
        photo_component: :class:`.PicovicoPhoto` instance.
        video_component: :class:`.PicovicoVideo` instance.
        music_component: :class:`.PicovicoMusic` instance.
        style_component: :class:`.PicovicoStyle` instance.
        project: :class:`.PicovicoProject` instance.

    Note:
        Components and Projects are available only after authorization.

    Args:
        app_id(str): Application ID given by Picovico.
        device_id(str): Some Device identifier. [Default  will be used]
        app_secret(str): *Optional* If  application secret is given.
    """

    def __init__(self, app_id, device_id=None, app_secret=None):
        super(PicovicoAPI, self).__init__(app_id, device_id=device_id, app_secret=app_secret)
        if self.is_authorized():
            self._pv_request.headers = self.headers
        self.__project = None
        self._ready_component_property()

    def login(self, username, password):
        """ API login method.
        Calls login action on API and sets access headers.
        Also, it readies the component attributes if everything ok.

        Args:
            username(str): Picovico login username.
            password(str): Picovico login password.
        """

        assert username, 'username is required for login'
        assert password, 'password is required for login'
        data = {
            'username': username,
            'password': password,
            'app_id' : self.app_id,
            'device_id': self.device_id
        }
        response = self._pv_request.post(path=pv_urls.PICOVICO_LOGIN, post_data=data)
        self.set_access_tokens(access_key=response.get('access_key'),
                    access_token=response.get('access_token'))
        self._pv_request.headers = self.headers
        self._ready_component_property()

    def __is_set_header(self):
        if self.is_authorized():
            self._pv_request.headers = self.headers
            return True
        return False

    def authenticate(self, app_secret=None):
        """ API authentication workflow.

        This is application secret based authentication.
        This also sets access headers and readies components.

        Args:
            app_secret(str): Application Secret provided by Picovico.
        """
        assert app_secret, 'App secret provided by picovico is required'
        if app_secret is not None and not self.app_secret:
            self._set_app_secret(app_secret)
        data={
            'app_id': self.app_id,
            'app_secret': self.app_secret,
            'device_id': self.device_id
        }
        response = self._pv_request.post(path=pv_urls.PICOVICO_APP, post_data=data)
        self.set_access_tokens(access_key=response.get('access_key'),
                access_token=response.get('access_token'))
        self._ready_component_property()

    @pv_auth_required
    def me(self):
        """ Get my profile.
        """
        return self._pv_request.get(path=pv_urls.ME)

    @property
    def project(self):
        return self.__project

    def _ready_component_property(self):
        if self.__is_set_header():
            self.__project = pv_project.PicovicoProject(self._pv_request)
            super(PicovicoAPI, self)._ready_component_property()

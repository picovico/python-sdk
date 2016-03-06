from .session import PicovicoSessionMixin
from .components import PicovicoComponentMixin
from .decorators import pv_auth_required
from . import urls as pv_urls
from . import project as pv_project


class PicovicoAPI(PicovicoSessionMixin, PicovicoComponentMixin):
    """ Picovico-SDK: The API class
    This class is base class for api activity. This class has all the attributes of
    componentmixin and sessinmixin. It will ready component and project objects based
    on authorization.

    Attributes(Only when you are authorized):
        project
        photo_component
        video_component
        music_component
        style_component

    Args:
        app_id(str): Application ID given by Picovico.
        device_id(str): Some Device identifier. [Default  will be used]
        app_secret(optional[str]): If  application secret is given
    """
    def __init__(self, app_id, device_id, app_secret=None):
        super(PicovicoAPI, self).__init__(app_id, device_id=device_id, app_secret=app_secret)
        self.__project = None
        if self.is_authorized():
            self._ready_component_property()
            self.__ready_project()

    def login(self, username, password):
        """ API login method.
        Calls  login action on API and sets access headers.
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
        self.__ready_project()

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
        self._pv_request.headers = self.headers
        self._ready_component_property()
        self.__ready_project()

    @pv_auth_required
    def me(self):
        """ Profile call from api.
        """
        return self._pv_request.get(path=pv_urls.ME)

    @property
    def project(self):
        """ Project Component.
        If authorized PicovicoProject object else None.
        """
        return self.__project


    def __ready_project(self):
        if self.is_authorized():
            self.__project = pv_project.PicovicoProject(self._pv_request)

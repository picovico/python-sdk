from .session import PicovicoSessionMixin
from .baserequest import PicovicoRequest
from .components import PicovicoComponentMixin
from .decorators import pv_auth_required
from . import urls as pv_urls

class PicovicoAPI(PicovicoSessionMixin, PicovicoComponentMixin):

    def __init__(self, app_id, device_id, app_secret=None):
        super(PicovicoAPI, self).__init__(app_id, device_id=device_id, app_secret=app_secret)
        PicovicoComponentMixin.__init__(self)
        if self.is_authorized():
            self._ready_component_property()


    def login(self, username, password):
        """ Picovico: login with username and password """
        assert username, 'username is required for login'
        assert password, 'password is required for login'
        data = {
            'username': username,
            'password': password,
            'app_id' : self.app_id,
            'device_id': self.device_id
        }
        response = self._pv_request.post(url=pv_urls.PICOVICO_LOGIN, post_data=data)
        self.set_access_tokens(access_key=response.get('access_key'),
                    access_token=response.get('access_token'))
        self._pv_request.headers = self.headers
        self._ready_component_property()

    def authenticate(self, app_secret=None):
        assert app_secret, 'App secret provided by picovico is required'
        if app_secret is not None and not self.app_secret:
            self._set_app_secret(app_secret)
        data={
            'app_id': self.app_id,
            'app_secret': self.app_secret,
            'device_id': self.device_id
        }
        response = self._pv_request.post(url=pv_urls.PICOVICO_APP, post_data=data)
        self.set_access_tokens(access_key=response.get('access_key'),
                access_token=response.get('access_token'))
        self._pv_request.headers = self.headers
        self._ready_component_property()

    @pv_auth_required
    def me(self):
        return self._pv_request.get(url=pv_urls.ME)

# from lib.api import PicovicoAPIRequest
# from lib import urls, exceptions, messages

DEFAULT_DEVICE_ID = "com.picovico.api.python-sdk"

class PicovicoSessionMixin(object):
    '''
        Picovico: Picovico class for picovico session like authentication, login and logout.
        Args:
            app_id(str): App ID provided by picovico
            app_secret(str): App Secret provided by picovico
    '''

    def __init__(self, app_id, app_secret=None, device_id=DEFAULT_DEVICE_ID):
        '''
            Picovico: Constructor that initialize the app_id and app_secret.
        '''
        super(PicovicoSessionMixin, self).__init__()
        self.__app_id = app_id
        self.__app_secret = app_secret
        self.__access_key = None
        self.__access_token = None
        self.__device_id = device_id

    @property
    def device_id(self):
        return self.__device_id

    @device_id.setter
    def device_id(self, value):
        self.__device_id  = value

    @property
    def access_key(self):
        return self.__access_key

    @property
    def access_token(self):
        return self.__access_token

    @property
    def app_id(self):
        return self.__app_id

    @property
    def app_secret(self):
        return self.__app_secret
        
    def _set_app_secret(self, app_secret):
        self.__app_secret = app_secret

    def set_access_tokens(self, access_key, access_token):
        '''
            Picovico: Set access_key and access_token as authentication key
            Args:
                access_key(str): access key provided by picovico
                access_token(str): access token provided by picovico
        '''
        self.__access_key = access_key
        self.__access_token = access_token

    def  is_anonymous(self):
        return not (self.access_key and self.access_token)

    def is_authorized(self):
        return not self.is_anonymous()

    @property
    def headers(self):
        if self.is_authorized():
            return {
                'X-Access-Key': self.access_key,
                'X-Access-Token': self.access_token
            }

    def logout(self):
        '''Picovico: Logout user'''
        self.set_access_tokens(None, None)
    

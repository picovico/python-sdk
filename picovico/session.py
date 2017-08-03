#: Picovico-SDK: default device identifier to be used.
DEFAULT_DEVICE_ID = "com.picovico.api.python-sdk"

class PicovicoSessionMixin(object):
    """ Picovico-SDK: **SessionMixin** class.

    This class itself is not useful.
    It provides API related session properties and method.

    Args:
        app_id (str): Application ID provided by picovico.
        app_secret (str, optional): Application Secret if avilable.
        devide_id (str, optional): Device Identication. Default value is :data:`.DEFAULT_DEVICE_ID`.
    """

    def __init__(self, app_id, app_secret=None, device_id=DEFAULT_DEVICE_ID):
        super(PicovicoSessionMixin, self).__init__()
        self.__app_id = app_id
        self.__app_secret = app_secret
        self.__access_key = None
        self.__access_token = None
        self.__device_id = device_id

    @property
    def device_id(self):
        """ Device Idetifier to be used.
        """
        return self.__device_id

    @device_id.setter
    def device_id(self, value):
        self.__device_id  = value

    @property
    def access_key(self):
        """ Read-Only Access Key.
        """
        return self.__access_key

    @property
    def access_token(self):
        """ Read-Only Access Token.
        """
        return self.__access_token

    @property
    def app_id(self):
        """ Read-Only Application ID provided during initiation.
        """
        return self.__app_id

    @property
    def app_secret(self):
        """ Read-Only Application Secret.
        """
        return self.__app_secret

    def _set_app_secret(self, app_secret):
        """ **Not for User.
        Sets application secret.
        """
        self.__app_secret = app_secret

    def set_access_tokens(self, access_key, access_token):
        """ Set access_key and access_token for authentication
        
        Args:
            access_key (str): access key provided by picovico
            access_token (str): access token provided by picovico
        """
        self.__access_key = access_key
        self.__access_token = access_token

    def  is_anonymous(self):
        """ Check if key and token are set.
        This should be opposite of is_authorized.

        Returns:
            bool: *True* if access_key and access_token is set else *False*.
        """
        return not (self.access_key and self.access_token)

    def is_authorized(self):
        """ Check if key and token are set.

        Returns:
            bool: *False* if is_anonymous else *True*.
        """
        return not self.is_anonymous()

    @property
    def auth_headers(self):
        """ Header dict based on is_authorized else None.
        """
        if self.is_authorized():
            return {
                'X-Access-Key': self.access_key,
                'X-Access-Token': self.access_token
            }

    def logout(self):
        """ Flush access key and token.
        """
        self.set_access_tokens(None, None)


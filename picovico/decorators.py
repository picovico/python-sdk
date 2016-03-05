import functools
from . import exceptions as pv_exceptions


def pv_auth_required(func):
    """ Picovico-SDK: Authentication necessity decorator.

    This decorator checks for object methods such as `is_authorized` and `is_authenticated`.
    It is mostly used with component and api class.
    Also it sets header to `_pv_request` attribute of the object.

    Raises:
        PicovicoAPINotAllowed
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        is_auth = getattr(self, 'is_authorized', self._pv_request.is_authenticated)
        if not is_auth():
            raise pv_exceptions.PicovicoAPINotAllowed('You cannot call this method without login or authenticate.')
        if hasattr(self, 'headers'):
            self._pv_request.headers = self.headers
        return func(self, *args, **kwargs)
    return wrapper


def pv_not_implemented(against):
    """ Picovico-SDK: Checks Implementation.

    Used in component class to check if
    the object component is implemented in API or not.

    Args:
        againsts(iterator): The check itertor.

    Raises:
        NotImplementedError
    """
    def func_wrapper(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            if self.component not in against:
                raise NotImplementedError
            return func(self, *args, **kwargs)
        return wrapper
    return func_wrapper


def pv_project_check_begin(func):
    """ Picovico-SDK: Check Project Initiation.

    This checks project object `video` attribute.

    Raises:
        PicovicoProjectNotAllowed
    """
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        if not self.video:
            raise pv_exceptions.PicovicoProjectNotAllowed('You should first begin the project')
        return func(self, *args, **kwargs)
    return wrapper
#def pv_auth_exempt(func):
    #""" Picovico: Authentication exemption decorator to be used with mixins. """
    #@functools.wraps(func)
    #def wrapper(self, *args, **kwargs):
        #ns.PicovicoAPINotAllowed('You cannot call this method without login or authenticate.')
        #self._pv_request.headers = self.headers
        #return func(self, *args, **kwargs)
    #return wrapper

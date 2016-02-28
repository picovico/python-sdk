import functools
from . import exceptions as pv_exceptions


def pv_auth_required(func):
    """ Picovico: Authentication necessity decorator to be used with mixins. """
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
    def func_wrapper(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            class_name = type(self).__name__.lower()
            print class_name
            if not any(class_name.endswith(a) for a in against):
                raise NotImplementedError
            return func(self, *args, **kwargs)
        return wrapper
    return func_wrapper

#for  project whether its  already begun or  not
def pv_project_check_begin(func):
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

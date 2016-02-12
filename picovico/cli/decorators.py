import functools

from . import profile_utils
from . import prompt

auth_login_msg = '''You are using {0} method but have {1} stored.
                    Your {1} will be overridden.'''

def pv_cli_check_authenticate(func):
    @functools.wraps(func)
    def wrapper(profile_name, *args, **kwargs):
        profile_name = profile_name or profile_utils.DEFAULT_PROFILE_NAME
        profile = profile_utils.get_profile(profile_name)
        if profile.APP_SECRET:
            prompt.show_warning(auth_login_msg.format('login', 'authentication'))
        f = func(profile_name, profile, *args, **kwargs)
        profile_utils.remove_profile_value(profile.NAME, profile.APP_SECRET)
        return f
    return wrapper

def pv_cli_check_login(func):
    @functools.wraps(func)
    def wrapper(profile_name, *args, **kwargs):
        profile_name = profile_name or profile_utils.DEFAULT_PROFILE_NAME
        profile = profile_utils.get_profile(profile_name)
        if profile.USERNAME:
            prompt.show_warning(auth_login_msg.format('authentication', 'login'))
        f = func(profile_name, profile, *args, **kwargs)
        profile_utils.remove_profile_value(profile.NAME, profile.USERNAME)
        return f
    return wrapper

#def pv_cli_session_required(func):
    #""" Picovico: Authentication necessity decorator to be used with mixins. """
    #@functools.wraps(func)
    #def wrapper(*args, **kwargs):
        #if not profile_utils.check_session_file():
            #if args == 'login':
                #prompt.
            

#def pv_not_implemented(against):
    #def func_wrapper(func):
        #@functools.wraps(func)
        #def wrapper(self, *args, **kwargs):
            #if self.component not in against:
                #raise NotImplementedError
            #return func(self, *args, **kwargs)
        #return wrapper
    #return func_wrapper
        
#def pv_auth_exempt(func):
    #""" Picovico: Authentication exemption decorator to be used with mixins. """
    #@functools.wraps(func)
    #def wrapper(self, *args, **kwargs):
        #ns.PicovicoAPINotAllowed('You cannot call this method without login or authenticate.')
        #self._pv_request.headers = self.headers
        #return func(self, *args, **kwargs)
    #return wrapper

import sys
import functools

from . import profile_utils
from . import prompt

def pv_cli_check_authenticate(func):
    @functools.wraps(func)
    def wrapper(profile_name, *args, **kwargs):
        profile_name = profile_name or profile_utils.DEFAULT_PROFILE_NAME
        profile = profile_utils.get_profile(profile_name)
        secret = getattr(profile, 'APP_SECRET', None)
        if secret:
            prompt.show_warning(auth_login_msg.format('login', 'authentication'))
        f = func(profile_name, profile, *args, **kwargs)
        if secret:
            profile_utils.remove_profile_value(profile.NAME, secret)
        return f
    return wrapper

def pv_cli_check_login(func):
    @functools.wraps(func)
    def wrapper(profile_name, *args, **kwargs):
        profile_name = profile_name or profile_utils.DEFAULT_PROFILE_NAME
        profile = profile_utils.get_profile(profile_name)
        username = getattr(profile, 'USERNAME', None)
        if username:
            prompt.show_warning(auth_login_msg.format('authentication', 'login'))
        f = func(profile_name, profile, *args, **kwargs)
        if username:
            profile_utils.remove_profile_value(profile.NAME, username)
        return f
    return wrapper

def pv_cli_check_configure(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        action = kwargs.pop('action')
        profile_name = kwargs.pop('profile', None) or profile_utils.DEFAULT_PROFILE_NAME
        if action != 'configure':
            try:
                profile_utils.get_profile(profile_name, info=True)
            except AssertionError:
                prompt.show_warning(prompt.NO_PROFILE_MSG, stop=True)
        return func(action, profile_name, *args, **kwargs)
    return wrapper


def pv_cli_check_info(funcname):
    def check(func):
        @functools.wraps(func)
        def wrapper(profile_name, *args, **kwargs):
            profile_name = profile_name or profile_utils.DEFAULT_PROFILE_NAME
            keyargs, removal, formatargs = profile_utils.get_auth_check_and_removal(funcname, profile_name)
            if kwargs:
                kwargs.update(keyargs)
            else:
                kwargs = keyargs
            if removal:
                prompt.show_auth_login_msg(formatargs)
            f = func(profile_name, *args, **kwargs)
            if removal:
                for rem in removal:
                    profile_utils.remove_profile_value(profile.NAME, rem)
            return f
        return wrapper
    return check

#def pv_cli_check_for_configure(func):
    #@functools.wraps(func)
    #def wrapper(profile_name, *args, **kwargs):
        #profile_name = profile_name or profile_utils.DEFAULT_PROFILE_NAME
        #has_login = kwargs.get('login', False)
        #has_authenticate = kwargs.get('authenticate', False)
        #auth_names = profile_utils.get_auth_names(profile_name)
        #override = None
        #if has_authenticate and not has_login:
            #against = profile_utils.AUTHENTICATE_INFO
            #override = profile_utils.LOGIN_INFO
        #if has_login and not has_authenticate:
            #against = profile_utils.LOGIN_INFO
            #override = profile_utils.AUTHENTICATE_INFO
        #if auth_names and any(k in auth_names for k in against):
            #kwargs.update(override=override)
        #return func(profile-name, *args, **kwargs)
    #return wrapper

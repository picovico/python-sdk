import sys
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
    def wrapper(action, profile_name, *args, **kwargs):
        profile_name = profile_name or profile_utils.DEFAULT_PROFILE_NAME
        if action != 'configure':
            try:
                profile = profile_utils.get_profile(profile_name, info=True)
            except AssertionError:
                prompt.show_warning('No profile found. You should run configure', stop=True)
        return func(action, profile_name, *args, **kwargs)
    return wrapper

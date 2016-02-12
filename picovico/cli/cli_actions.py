import sys
import itertools

import six

from . import decorators as cli_dec
from . import profile_utils
from . import prompt
from .. import PicovicoAPI
from ..components.base import PicovicoBaseComponent




#other_actions = {
    #'session_actions': (
        #'get_my_profile',
        #'get_my_styles',
        #'get_my_musics',
        #'get_my_videos',
        #'get_my_photos'
    #),
    #'exempt_actions': (
        #'get_free_styles',
        #'get_free_musics'
    #),
#}
#action.update({for action in other_actions:
   

def prepare_api_object(profile, session=False):
    api = PicovicoAPI(profile.APP_ID, profile.DEVICE_ID)
    if session:
        sess = profile_utils.get_session_info()
        if sess.PROFILE == profile.NAME:
            api.set_access_tokens(sess.access_key, sess.ACCESS_TOKEN)
        else:
            msg = 'No session for profile: {}'.format(profile.NAME)
            msg += '\nEither login or authenticate this profile.'
            prompt.show_warning(msg)
            sys.exit(0)
    return api

def retry_once_for_assertions(func, **kwargs):
    try:
        value = func(**kwargs)
    except AssertionError as e:
        prompt.show_warning(e.message)
        value = func(**kwargs)
    return value

def override_configure(profile_name, login=False, authenticate=False):
    prompt.show_warning('Your existing profile [] will be overriden.'.format(profile_name))
    configure(profile_name, login, authenticate)

def configure(profile_name=None, login=False, authenticate=False):
    profile_name = profile_name or profile_utils.DEFAULT_PROFILE_NAME
    info = {}
    #info.update(PROFILE=profile_name)
    info['APP_ID'], info['DEVICE_ID'] = retry_once_for_assertions(prompt.configure_prompt)
    if login:
        info['USERNAME'], info['PASSWORD'] = retry_once_for_assertions(prompt.configure_login_info)
    elif authenticate:
        info['APP_SECRET'] = retry_once_for_assertions(prompt.configure_secret_info)
    is_set = profile_utils.set_profile(info, profile_name)
    if is_set:
        prompt.show_print('Congratulation. You have configured picovico. Run API actions.')
        prompt.show_print('You have the following profile:')
        for profile in profile_utils.get_all_profiles():
            prompt.show_print(profile)
    else:
        prompt.show_print('Something unknown happened. Rerun configure')


def auth_action(funcname, profile_name, *args):
    if isinstance(profile_name, six.string_types) or not profile_name:
        profile_name = profile_name or profile_utils.DEFAULT_PROFILE_NAME
        profile = profile_utils.get_profile(profile_name)
    api = prepare_api_object(profile)
    getattr(api, funcname)(*args)
    if api.is_authorized():
        data = {
            'ACCESS_KEY': api.access_key,
            'ACCESS_TOKEN': api.access_token,
            'PROFILE': profile.NAME
        }
        file_utils.write_to_session_file(data)
    

@cli_dec.pv_cli_check_authenticate
def login(profile_name, profile=None):
    username, password = retry_once_for_assertions(prompt.configure_login_info, coerce_password=True)
    auth_action('login', profile or profile_name, username, password)

@cli_dec.pv_cli_check_login
def authenticate(profile_name, profile=None):
    app_secret = retry_once_for_assertions(prompt.configure_secret_info)
    auth_action('authenticate', profile or profile_name, app_secret)

#def call_session_actions(action, profile_name):
    #profile_name = profile_name or profile_utils.DEFAULT_PROFILE_NAME
    #api = prepare_api_object()
    #profile = profile_utils.get_profile(profile_name)
    

#def map_action_to_api(action, profile_name):
    #if action not in :
    
prompt_actions = {
    'configure': configure,
    'login': login,
    'authenticate': authenticate,
}
component_actions = {
    'music_component': ('get_musics', 'get_music', 'delete_music', 'get_free_musics'),
    'photo_component': ('get_photos', 'get_photo', 'delete_photo'),
    'video_component': ('get_videos', 'get_video', 'delete_video'),
    'style_component': ('get_styles', 'get_free_styles')
}
exempt_actions = ('get_free_musics', 'get_free_styles')
component_action_names = six.itervalues(component_actions)
exempt_id_actions = (v[0] for v in component_action_names)
all_actions = itertools.chain(six.iterkeys(prompt_actions), *component_action_names)

import sys
import itertools

import six

from . import decorators as cli_dec
from . import profile_utils
from . import prompt
from .. import PicovicoAPI
from ..components.base import PicovicoBaseComponent
from .. import exceptions as pv_api_exceptions


# component_actions = ('get_musics', 'get_music', 'delete_music',
                        # 'get_free_musics', 'get_photos', 'get_photo',
                        # 'delete_photo', 'get_videos', 'get_video',
                        # 'delete_video', 'get_styles', 'get_free_styles')
# no_auth_actions = ('get_free_styles', 'get_free_musics')

def prepare_api_object(profile_name, session=False):
    profile_name = profile_name or profile_utils.DEFAULT_PROFILE_NAME
    profile = profile_utils.get_profile(profile_name, info=True)
    api = PicovicoAPI(profile.APP_ID, profile.DEVICE_ID)
    if session:
        sess = profile_utils.get_session_info()
        if sess and sess.PROFILE == profile.NAME:
            api.set_access_tokens(sess.access_key, sess.ACCESS_TOKEN)
        else:
            auth_names = profile_utils.get_auth_names(profile.NAME)
            sess = getattr(profile, auth_name, None)
            action = {
                profile_utils.LOGIN_INFO: 'login',
                profile_utils.AUTHENTICATE_INFO: 'authenticate',
            }.get(auth_name, None)
            if not sess:
                prompt.show_no_session()
            else:
                arguments = {k.lower(): getattr(profile, k) for k in auth_names}
                api = auth_action(action, profile, **arguments)
    return api

def retry_once_for_assertions(func, **kwargs):
    try:
        value = func(**kwargs)
    except AssertionError as e:
        prompt.show_warning(e.message)
        value = func(**kwargs)
    return value

def configure_login_authenticate(profile_name, login=False, authenticate=False):
    info = {}
    remove_info = None
    if login:
        info['USERNAME'], info['PASSWORD'] = retry_once_for_assertions(prompt.configure_login_info)
        remove_info = profile_utils.AUTHENTICATE_INFO
    elif authenticate:
        info['APP_SECRET'] = retry_once_for_assertions(prompt.configure_secret_info)
        remove_info = profile_utils.LOGIN_INFO
    if remove_info:
        for inf in remove_info:
            profile_utils.remove_profile_value(profile_name, inf)
    return info

def configure(profile_name=None, login=False, authenticate=False):
    profile_name = profile_name or profile_utils.DEFAULT_PROFILE_NAME
    info = {}
    info['APP_ID'], info['DEVICE_ID'] = retry_once_for_assertions(prompt.configure_prompt)
    remove_info = None
    all_profiles = profile_utils.get_all_profiles()
    if profile_name in all_profiles:
        prompt.show_warning('Your existing profile [] will be overriden.'.format(profile_name))
    info.update(configure_login_authenticate(profile_name, login, authenticate))
    is_set = profile_utils.set_profile(info, profile_name)
    if is_set:
        prompt.show_print('Congratulation. You have configured picovico. Run API actions.')
        prompt.show_print('You have the following profile:')
        for profile in profile_utils.get_all_profiles():
            prompt.show_print(profile)
    else:
        prompt.show_print('Something unknown happened. Rerun configure')


def auth_action(funcname, profile_name, **kwargs):
    profile_name = getattr(profile_name, 'NAME', profile_name)
    api = prepare_api_object(profile_name)
    getattr(api, funcname)(*args)
    if api.is_authorized():
        data = {
            'ACCESS_KEY': api.access_key,
            'ACCESS_TOKEN': api.access_token,
            'PROFILE': profile_name
        }
        file_utils.write_to_session_file(data)
    return api

def my_profile(profile_name):
    api = prepare_api_object(profile_name, session=True)
    return api.me()

@cli_dec.pv_cli_check_authenticate
def login(profile_name, profile=None):
    username, password = retry_once_for_assertions(prompt.configure_login_info, coerce_password=True)
    auth_action('login', profile or profile_name, username=username, password=password)

@cli_dec.pv_cli_check_login
def authenticate(profile_name, profile=None):
    app_secret = retry_once_for_assertions(prompt.configure_secret_info)
    auth_action('authenticate', profile or profile_name, app_secret=app_secret)

def logout(profile_name):
    api = prepare_api_object(profile_name)
    api.logout()
    file_utils.delete_session_file()

def get_action_from_command(action, profile_name):
    action_maps = cli_map_command_to_actions()
    action_map = action_maps.get(action)
    current_action = action_map.get('action')
    component = action_map.get('component', None)
    if component:
        api = prepare_api_object(profile_name, session=True)
        component = getattr(api, component)
        current_action = getattr(component, current_action)
    return current_action

@cli_dec.pv_cli_check_configure
def call_api_actions(action, profile_name, **arguments):
    current_action = get_action_from_command(action, profile_name)
    try:
        result = api_action(**arguments)
    except (pv_api_exceptions.PicovicoRequestError, pv_api_exceptions.PicovicoServerError) as  e:
        prompt.show_action_error(action, profile_name, e.status, e.message)
    else:
        if result:
            prompt.show_action_result(action, result, profile_name)
        else:
            prompt.show_action_success(action, profile_name)

def component_commands():
    components = PicovicoBaseComponent._components
    exclude_for_delete_component = (components[0],)
    has_free_component = components[:2]
    component_map = []
    for component in PicovicoBaseComponent._components:
        command = 'get-{}s'.format(component)
        action = 'get_{}s'.format(component)
        component_map.append({'command': command, 'options': None, 'action': action, 'component': '{}_component'.format(component)})
        if component not in exclude_for_delete_component:
            command = 'get-{}'.format(component)
            action = 'get_{}'.format(component)
            component_map.append({'command': command, 'options': [{'name': '--{}-id'.format(component), 'required': True}], 'action': action, 'component': '{}_component'.format(component)})
            command = 'delete-{}'.format(component)
            action = 'delete_{}'.format(component)
            component_map.append({'command': command, 'options': [{'name': '--{}-id'.format(component), 'required': True}], 'action': action, 'component': '{}_component'.format(component)})
    for component in has_free_component:
        command = 'get-free-{}s'.format(component)
        action = 'get_free_{}s'.format(component)
        component_map.append({'command': command, 'options': None, 'action': action, 'component': '{}_component'.format(component)})
    return component_map

def get_cli_commands():
    commands = [
        {'command': 'configure', 'options': [{'name': '--use', 'choices': ('login', 'authenticate'), 'required': False}]},
        {'command': 'login', 'options': None},
        {'command': 'logout', 'options': None},
        {'command': 'authenticate', 'options': None},
        {'command': 'my-profile', 'options': None},
    ]
    components = component_commands()
    commands = itertools.chain(commands, [{'command': d['command'], 'options': d['options']} for d in components])
    all_commands = [profile_utils._create_namedtuple('CliCommandsConfig', d) for d in commands]
    return all_commands

def cli_map_command_to_actions():
    command_action_map = {
        'configure': {'action': configure},
        'login': {'action': login},
        'logout': {'action': logout},
        'authenticate': {'action': authenticate},
        'my-profile': {'action': my_profile},
    }
    components = component_commands()
    command_action_map.update({d['action']: {'action': d['action'], 'component': d['component']} for d in components})
    return command_action_map

import sys
import itertools

import six

from . import decorators as cli_dec
from . import log as cli_logger
from . import profile_utils
from . import prompt
from . import project_driver as proj_driver
from . import utils as pv_utility
from .. import PicovicoAPI
from ..components.base import PicovicoBaseComponent
from .. import exceptions as pv_api_exceptions

custom_command = ('login', 'logout', 'authenticate', 'configure', 'my_profile')
# component_actions = ('get_musics', 'get_music', 'delete_music',
                        # 'get_free_musics', 'get_photos', 'get_photo',
                        # 'delete_photo', 'get_videos', 'get_video',
                        # 'delete_video', 'get_styles', 'get_free_styles')
# no_auth_actions = ('get_free_styles', 'get_free_musics')

def configure_login_authenticate(profile_name, login=False, authenticate=False):
    info = {}
    remove_info = None
    if login:
        info['USERNAME'], info['PASSWORD'] = prompt.retry_once_for_assertions(prompt.configure_login_info)
        remove_info = profile_utils.AUTHENTICATE_INFO
        if not info['PASSWORD']:
            info.pop('PASSWORD')
    elif authenticate:
        info['APP_SECRET'] = prompt.retry_once_for_assertions(prompt.configure_secret_info)
        remove_info = profile_utils.LOGIN_INFO
    if remove_info:
        for inf in remove_info:
            profile_utils.remove_profile_value(profile_name, inf)
    return info

def configure(profile_name=None, login=False, authenticate=False, log=False):
    profile_name = profile_name or profile_utils.DEFAULT_PROFILE_NAME
    info = {}
    info['APP_ID'], info['DEVICE_ID'] = prompt.retry_once_for_assertions(prompt.configure_prompt)
    remove_info = None
    all_profiles = profile_utils.get_all_profiles()
    if profile_name in all_profiles:
        prompt.show_warning('Your existing profile "{}" will be overriden.\n'.format(profile_name))
    info.update(configure_login_authenticate(profile_name, login, authenticate))
    info.update(LOG=log)
    is_set = profile_utils.set_profile(info, profile_name)
    if is_set:
        prompt.show_print('Congratulation. You have configured picovico. Run API actions.')
        prompt.show_print('You have the following profile:')
        for profile in profile_utils.get_all_profiles():
            prompt.show_print(profile)
    else:
        prompt.show_print('Something unknown happened. Rerun configure')

def my_profile(profile_name=None):
    api = pv_utility.prepare_api_object(profile_name, session=True)
    return api.me()

@cli_dec.pv_cli_check_info('login')
def login(profile_name=None, username=None, password=None, profile=None, do_prompt=True):
    if do_prompt and not (username and password):
        username, password = prompt.retry_once_for_assertions(prompt.configure_login_info, coerce_password=True)
    if username and not password:
        password = prompt.retry_once_for_assertions(prompt.configure_password_info)
    profile_name = getattr(profile, 'NAME', profile_name)
    pv_utility.auth_action('login', profile_name, username=username, password=password)

@cli_dec.pv_cli_check_info('authenticate')
def authenticate(profile_name=None, app_secret=None, profile=None, do_prompt=True):
    if do_prompt and not app_secret:
        app_secret = prompt.retry_once_for_assertions(prompt.configure_secret_info)
    profile_name = getattr(profile, 'NAME', profile_name)
    pv_utility.auth_action('authenticate', profile_name, app_secret=app_secret)

def logout(profile_name=None):
    api = pv_utility.prepare_api_object(profile_name, session=True)
    api.logout()
    file_utils.delete_session_file()

def get_action_from_command(action, profile_name):
    action_maps = cli_map_command_to_actions()
    action_map = action_maps.get(action)
    current_action = action_map.get('action')
    component = action_map.get('component', None)
    if component:
        api = pv_utility.prepare_api_object(profile_name, session=True)
        component = getattr(api, component)
        current_action = getattr(component, current_action)
    return current_action

@cli_dec.pv_cli_check_configure
def call_api_actions(action, profile, **kwargs):
    assert action, 'State your command'
    api_action = get_action_from_command(action, profile)
    if action in custom_command:
        if kwargs:
            kwargs.update({'profile_name': profile})
        else:
            kwargs = {'profile_name': profile}
    try:
        result = api_action(**kwargs)
    except (pv_api_exceptions.PicovicoRequestError, pv_api_exceptions.PicovicoServerError) as  e:
        prompt.show_action_error(action, profile, e.status, e.message)
    else:
        if result:
            prompt.show_action_result(action, result, profile)
        else:
            prompt.show_action_success(action, profile)
    prof = profile_utils.get_profile(profile)
    if prof.LOG and action not in custom_command:
        cli_logger.log_actions(prof.NAME, action, result, **kwargs)

def create_component_commands():
    #components = {
        #'music': {'get-{}s': [], 'get-{}': [{'name': '--music-id', 'required': True}], 'upload-{}-file': [{'name': '--filename', 'required': True}], 'upload-{}-url': [{'name': '--{}'.format(opt), 'required': True} for opt in ('url', 'preview')], 'delete-{}':  [{'name': '--music-id', 'required': True}], 'get-free-{}s': []},
        #'style': {'get-{}s': [], 'get-{}': [], 'get-free-{}s': []},
        #'photo': {'get-{}s': [], 'get-{}': [{'name': '--photo-id', 'required': True}], 'upload-{}-file': [{'name': '--filename', 'required': True}], 'upload-{}-url': [{'name': '--{}'.format(opt), 'required': True} for opt in ('url', 'tumbnail')], 'delete-{}':  [{'name': '--photo-id', 'required': True}]},
        #'video': {'get-{}s': [], 'get-{}': [{'name': '--video-id', 'required': True}], 'delete-{}':  [{'name': '--video-id', 'required': True}]}
    #}
    all_components = PicovicoBaseComponent._components
    exclude_for_delete = all_components[:1]
    has_free_component = all_components[:2]
    upload_components = {
        'music': {'file': ['--filename'], 'url': ['--url', '--preview']},
        'photo': {'file': ['--filename'], 'url': ['--url', '--thumbnail']}
    }
    components = {}
    for component in all_components:
        components[component] = {
            'get-{}s'.format(component): []
        }
        cur_comp = components[component]
        component_id = '--{}-id'.format(component)
        if component not in exclude_for_delete:
            act = 'get-{}'.format(component)
            cur_comp.update({act: [{'name': component_id, 'required': True}]})
            act = 'delete-{}'.format(component)
            cur_comp.update({act: [{'name': component_id, 'required': True}]})
        if component in has_free_component:
            act = 'get-free-{}s'.format(component)
            cur_comp.update({act: []})
        if component in upload_components:
            for k, v in six.iteritems(upload_components[component]):
                act = 'upload-{}-{}'.format(component, k)
                cur_comp.update({act: [{'name': n, 'required':True} for n in v]})
    return components

def component_commands():
    components = create_component_commands()
    component_map = []
    for component, actions in six.iteritems(components):
        for method, options in six.iteritems(actions):
            command = method.format(component)
            action = command.replace('-', '_')
            component_map.append({'command': command, 'options': None, 'action': action, 'component': '{}_component'.format(component)})
            if options:
                command = method.format(component)
                action = command.replace('-', '_')
                component_map.append({'command': command, 'options':  options, 'action': action, 'component': '{}_component'.format(component)})
    return component_map

def get_cli_commands():
    commands = [
        {'command': 'configure', 'options': [{'name': '--with', 'choices': ('login', 'authenticate'), 'required': False, 'dest': 'include'}, {'name': '--log', 'action': 'store_true'}]},
        {'command': 'login', 'options': None},
        {'command': 'logout', 'options': None},
        {'command': 'authenticate', 'options': None},
        {'command': 'my-profile', 'options': None},
        {'command': 'flush-log', 'options': None}
    ]

    components = component_commands()
    commands = itertools.chain(commands, [{'command': d['command'], 'options': d['options']} for d in components])
    all_commands = [profile_utils._create_namedtuple('CliCommandsConfig', d) for d in commands]
    project_commands = proj_driver.get_project_cli_commands()
    all_commands = itertools.chain(all_commands, project_commands)
    return all_commands

def cli_map_command_to_actions():
    command_action_map = {
        'configure': {'action': configure},
        'login': {'action': login},
        'logout': {'action': logout},
        'authenticate': {'action': authenticate},
        'my-profile': {'action': my_profile},
        'flush-log': {'action': cli_logger.flush_log},
        'project': {'action': proj_driver.project_cli_action}
    }
    components = component_commands()
    command_action_map.update({d['action']: {'action': d['action'], 'component': d['component']} for d in components})
    return command_action_map

#import os
import errno
import itertools
import collections

import six

from . import file_utils
#from . import PicovicoAPI
#from .session import DEFAULT_DEVICE_ID
#from .exceptions import PicovicoCLIError, PicovicoProfileError

NECESSARY_INFO = ('APP_ID', 'DEVICE_ID')
AUTHENTICATE_INFO = ('APP_SECRET',)
LOGIN_INFO = ('USERNAME', 'PASSWORD')
SESSION_INFO = ('ACCESS_KEY', 'ACCESS_TOKEN', 'ID', 'PROFILE')
DEFAULT_PROFILE_NAME = six.moves.configparser.DEFAULTSECT
ALL_INFO = itertools.chain(NECESSARY_INFO, AUTHENTICATE_INFO, LOGIN_INFO)
#Profile = collections.namedtuple('Profile', itertools.chain(chained_info, ('NAME',)))

def check_against_factory(cfg, profile_name, against, check_value=False):
    has_section = (profile_name == DEFAULT_PROFILE_NAME)
    if not has_section:
        has_section = cfg.has_section(profile_name)
    if has_section:
        ok = all(cfg.has_option(profile_name, opt) for opt in against)
        if check_value and ok:
            ok = all(cfg.get(profile_name, opt) for opt in against)
        return ok
    return has_section

def has_necessary_info(cfg, profile_name):
    return check_against_factory(cfg, profile_name, NECESSARY_INFO)

def check_necessary_info_values(cfg, profile_name):
    return check_against_factory(cfg, profile_name, NECESSARY_INFO, check_value=True)

def has_authenticate_info(cfg, profile_name):
    return check_against_factory(cfg, profile_name, AUTHENTICATE_INFO)

def check_authenticate_info_value(cfg, profile_name):
    return check_against_factory(cfg, profile_name, AUTHENTICATE_INFO, check_value=True)

def _create_namedtuple(name, dict_to_make):
    Factory = collections.namedtuple(name, [m.upper() for m in six.iterkeys(dict_to_make)])
    return Factory._make(six.itervalues(dict_to_make))

def create_profile_values(list_of_values):
    ret_val = [_create_namedtuple('Conf', dict(six.moves.zip(('name', 'value'), val))) for val in list_of_values]
    return ret_val

def set_profile(values_to_set, profile_name):
    cfg = get_raw_profile(profile_name)
    if isinstance(values_to_set, dict):
        copied_value = values_to_set.copy()
        values_to_set = create_profile_values(six.iteritems(copied_value))
    for value in values_to_set:
        cfg.set(profile_name, value.NAME, str(value.VALUE))
    profile_file = file_utils.get_profile_file()
    f = file_utils.get_file_obj(profile_file, mode='w')
    if f:
        with f:
            cfg.write(f)
            return True
    return False

def write_new_profile_info(cfg, profile_name):
    profile_file = file_utils.get_profile_file()
    fp = file_utils.get_file_obj(profile_file, mode='w+')
    if fp:
        write = False
        if profile_name != DEFAULT_PROFILE_NAME \
            and profile_name not in cfg.sections():
            cfg.add_section(profile_name)
            write = True
        if not check_necessary_info_values(cfg, profile_name):
            for opt in NECESSARY_INFO:
                cfg.set(profile_name, opt, '')
            write = True
        if write:
            with fp:
                cfg.write(fp)
    #if not check_necessary_info_values(cfg, profile_name):
        #for opt in NECESSARY_INFO:
            #cfg.set(profile_name, opt, '')
                #cfg.write(fp)

def get_raw_profile(profile_name=DEFAULT_PROFILE_NAME):
    profile_file = file_utils.get_profile_file()
    fp = file_utils.get_file_obj(profile_file)
    cfg = None
    if fp:
        cfg = six.moves.configparser.SafeConfigParser()
        #cfg.optionxform = str
        with fp:
            cfg.readfp(fp)
        write_new_profile_info(cfg, profile_name)
    return cfg

def remove_profile_value(profile_name, option):
    cfg = get_raw_profile(profile_name)
    cfg.remove_option(profile_name, option)

def get_profile(profile_name):
    cfg = get_raw_profile(profile_name)
    if not cfg.sections():
       profile_name = DEFAULT_PROFILE_NAME
    options = dict(cfg.items(profile_name))
    options.update(name=profile_name)
    return _create_namedtuple('Profile', options)

def get_all_profiles():
    cfg = get_raw_profile()
    profiles = cfg.sections()
    if check_necessary_info_values(cfg, DEFAULT_PROFILE_NAME):
        profiles.append(DEFAULT_PROFILE_NAME)
    return profiles

def check_session_file():
    data = file_utils.read_from_session_file()
    if data:
        ok = all(k in data for k in SESSION_INFO)
        if ok:
            ok = all(six.itervalues(data))
        return ok
    return False

def get_session_info():
    if check_session_file():
        data = file_utils.read_from_session_file()
        return _create_namedtuple('Session', data)
        

#def get_configure_profile(profile_name=None, auth=False, login=False):
    #profile_info = {}
    #profile_info.update({k: None for k in Profile._fields})
    #profile_info.update(SECTION=profile_name or DEFAULT_SECTION_NAME)
    #profile_info['APP_ID'] = six.moves.input('Enter Application Id provided: ')
    #assert profile_info['APP_ID'] and isinstance(profile_info['APP_ID'], six.string_types)
    #profile_info['DEVICE_ID'] = six.moves.input('Enter Device Identifier->[default:{}]: '.format(DEFAULT_DEVICE_ID))
    #if not profile_info['DEVICE_ID']:
        #profile_info.update(DEVICE_ID=DEFAULT_DEVICE_ID)
    #if auth and not login:
        #profile_info['APP_SECRET'] = six.moves.input('Enter Application Secret: ')
        #assert profile_info['APP_SECRET'] and isinstance(profile_info['APP_SECRET'], six.string_types)
    #if login and not auth:
        #profile_info['USERNAME'] = six.moves.input('Enter Picovico Username: ')
        #assert profile_info['USERNAME']
        #profile_info['PASSWORD'] = six.moves.input('Enter Picovico Password[Will not be stored]: ')
        #assert profile_info['PASSWORD']
    #if profile_info['APP_SECRET'] or (profile_info['USERNAME'] and profile_info['PASSWORD']):
        #profile_info.update(AUTH=True)
    #return Profile(**profile_info)

#def set_configs(values_to_set, section_name=DEFAULT_SECTION_NAME, filename='profile.ini'):
    #cfg = get_config(filename, section_name)
    #for value in values_to_set:
        #cfg.set(section_name, value.attr, str(value.value))
    #cfg.write(open(filename, 'w'))

#def create_conf_values(list_of_values):
    #Conf = collections.namedtuple('Conf', 'attr value')
    #ret_val = []
    #for val in list_of_values:
        #ret_val.append(Conf._make(val))
    #return ret_val

#def write_access_info(profile_info):
    #if profile_info.APP_SECRET:
        #additional_conf = create_conf_values((('APP_SECRET', profile_info.APP_SECRET),))
    #else:
        #additional_conf = create_conf_values((('USERNAME', profile_info.USERNAME),))
    #set_configs(additional_conf, section_name=profile_info.SECTION)
    #api = PicovicoAPI(profile_info.APP_ID, profile_info.DEVICE_ID)
    #if profile_info.APP_SECRET:
        #api.authenticate(profile_info.APP_SECRET)
    #else:
        #api.login(profile_info.USERNAME, profile_info.PASSWORD)
    #additional_conf = create_conf_values(((v, getattr(api, v.lower())) for v in OPTIONAL_INFO_TOKEN))
    #set_configs(additional_conf, section_name=profile_info.SECTION)

#def configure(profile_name, auth_with=None):
    #key_args = {}
    #if auth_with == 'login':
        #key_args.update(login=True)
    #elif auth_with == 'secret':
        #key_args.update(auth=True)
    #profile_info = get_configure_profile(profile_name, **key_args)
    #necessary_conf = create_conf_values(((a, getattr(profile_info, a)) for a in NECESSARY_INFO))
    #set_configs(necessary_conf, section_name=profile_info.SECTION)
    #if profile_info.AUTH:
        #write_access_info(profile_info)


#def get_config_with_secret(profile_section='default'):
    #pass
    #cfg = get_config()
    #app_id = cfg.get('APP_ID')
#def get_config_with_token(profile_section='default'):
    #if not app_id:
        #raise PicovicoCLIError('No APP ID found.', code=0)
    #data = cfg.items(profile_section)


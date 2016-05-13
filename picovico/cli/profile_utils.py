import itertools
import collections

import six

from picovico.cli import file_utils


NECESSARY_INFO = ('APP_ID', 'DEVICE_ID')
AUTHENTICATE_INFO = ('APP_SECRET',)
LOGIN_INFO = ('USERNAME', 'PASSWORD')
SESSION_INFO = ('ACCESS_KEY', 'ACCESS_TOKEN', 'PROFILE')
DEFAULT_PROFILE_NAME = six.moves.configparser.DEFAULTSECT
ALL_INFO = itertools.chain(NECESSARY_INFO, AUTHENTICATE_INFO, LOGIN_INFO)

def check_against_factory(cfg, profile_name, against, check_value=False):
    has_section = (profile_name.upper() == DEFAULT_PROFILE_NAME) or cfg.has_section(profile_name)
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

def has_login_info(cfg, profile_name, both=False):
    check_against = LOGIN_INFO if both else LOGIN_INFO[:1]
    return check_against_factory(cfg, profile_name, check_against)

def check_login_info_value(cfg, profile_name, both=False):
    check_against = LOGIN_INFO if both else LOGIN_INFO[:1]
    return check_against_factory(cfg, profile_name, check_against, check_value=True)

def _create_namedtuple(name, dict_to_make):
    key_transformation = {k.upper(): v for k, v in six.iteritems(dict_to_make)}
    Factory = collections.namedtuple(name, six.iterkeys(key_transformation))
    return Factory(**key_transformation)

def create_profile_values(list_of_values):
    ret_val = [_create_namedtuple('Conf', dict(zip(('name', 'value'), val))) for val in list_of_values]
    return ret_val

def is_in_profile(values_to_check, profile_name):
    cfg = get_raw_profile()
    return check_against_factory(cfg, profile_name, values_to_check, check_value=True)

def set_profile(values_to_set, profile_name):
    cfg = get_raw_profile()
    write_new_profile_info(cfg, profile_name)
    if isinstance(values_to_set, dict):
        copied_value = values_to_set.copy()
        values_to_set = create_profile_values(six.iteritems(copied_value))
    for value in values_to_set:
        cfg.set(profile_name, value.NAME, str(value.VALUE))
    cfg = write_profile_config(cfg)
    if cfg:
        return True
    return False
    
def write_profile_config(cfg, mode='w'):
    profile_file = file_utils.get_profile_file()
    fp = file_utils.get_file_obj(profile_file, mode=mode)
    with fp:
        cfg.write(fp)
        return cfg

def write_new_profile_info(cfg, profile_name):
    if file_utils.has_profile_file():
        write = False
        if profile_name.lower() not in get_all_profiles():
            cfg.add_section(profile_name.lower())
            write = True
            # cfg = write_profile_config(cfg, mode='w+')
        if not check_necessary_info_values(cfg, profile_name):
            for opt in NECESSARY_INFO:
                cfg.set(profile_name, opt, '')
            write = True
        if write:
            cfg = write_profile_config(cfg, mode='w+')

def get_raw_profile():
    profile_file = file_utils.get_profile_file()
    fp = file_utils.get_file_obj(profile_file, 'rb')
    cfg = None
    if fp:
        cfg = six.moves.configparser.SafeConfigParser()
        with fp:
            cfg.readfp(fp)
    return cfg        

def remove_profile_value(profile_name, option):
    cfg = get_raw_profile()
    if cfg and cfg.has_option(profile_name, option):
        if cfg.remove_option(profile_name, option):
            write_profile_config(cfg, mode='w+')
            
def get_profile(profile_name, info=True):
    cfg = get_raw_profile()
    if not cfg:
        cfg = six.moves.configparser.SafeConfigParser()
        write_new_profile_info(cfg, profile_name)
    sections = cfg.sections()
    sections.append(DEFAULT_PROFILE_NAME.lower())
    if profile_name.lower() not in sections:
        raise ValueError('No Profile: {} found.'.format(profile_name))
    if info:
        assert check_necessary_info_values(cfg, profile_name)
    options = dict(cfg.items(profile_name))
    options.update(name=profile_name)
    return _create_namedtuple('Profile', options)

def get_all_profiles():
    cfg = get_raw_profile()
    profiles = []
    if cfg:
        profiles = cfg.sections()
        if check_necessary_info_values(cfg, DEFAULT_PROFILE_NAME):
            profiles.append(DEFAULT_PROFILE_NAME.lower())
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

def get_auth_names(profile_name):
    cfg = get_raw_profile()
    is_available = {
        check_authenticate_info_value(cfg, profile_name): AUTHENTICATE_INFO,
    }
    if True not in is_available and check_login_info_value(cfg, profile_name):
        is_available.update({True: LOGIN_INFO[:1]})
        if check_login_info_value(cfg, profile_name, both=True):
            is_available.update({True: LOGIN_INFO})
    return is_available.get(True, None)

def get_auth_check_and_removal(name, profile_name):
    auth_names = get_auth_names(profile_name)
    profile = get_profile(profile_name)
    names = ('login', 'authenticate')
    keyargs = {'do_prompt': True, 'profile': profile}
    remove = None
    if auth_names:
        to_remove = (AUTHENTICATE_INFO[0], LOGIN_INFO[0])
        to_check = (LOGIN_INFO, AUTHENTICATE_INFO)
        if not names.index(name):
            names = names[::-1]
            to_remove = to_remove[::-1]
            to_check = to_check[::-1]
        check_map = dict(zip(names, to_check))
        removal_map = dict(zip(names, to_remove))
        remove = removal_map.get(name)
        check = check_map.get(name)
        if any(k in check for k in auth_names):
            keyargs.update(do_prompt=False)
            keyargs.update({k.lower(): getattr(profile, k, None) for k in check})
        elif not any(k in remove for k in auth_names):
            remove = None
    return keyargs, remove, names

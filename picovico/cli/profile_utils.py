#import os
#import errno
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
DEFAULT_PROFILE_SECTION_NAME = six.moves.configparser.DEFAULTSECT
chained_info = itertools.chain(NECESSARY_INFO, AUTHENTICATE_INFO, LOGIN_INFO)
Profile = collections.namedtuple('Profile', itertools.chain(chained_info, ('NAME',)))

def check_against_factory(cfg, profile_name, against, check_value=False):
    has_section = (profile_name == DEFAULT_PROFILE_SECTION_NAME)
    if profile_name != DEFAULT_PROFILE_SECTION_NAME:
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

def create_profile_values(list_of_values):
    Conf = collections.namedtuple('Conf', 'name value')
    ret_val = [Conf._make(val) for val in list_of_values]
    return ret_val

def set_profile(cfg, values_to_set, profile_name):
    cfg = get_raw_profile(profile_name)
    for value in values_to_set:
        cfg.set(profile_name, value.name, str(value.value))
    profile_file = file_utils.get_profile_file()
    with open(profile_file, 'ab+') as f:
        cfg.write(f)

def get_raw_profile(profile_name=DEFAULT_PROFILE_SECTION_NAME):
    profile_file = file_utils.get_profile_file()
    fp = open(profile_file, 'ab+')
    cfg = six.moves.configparser.SafeConfigParser()
    with fp:
        cfg.readfp(fp)
        if profile_name != DEFAULT_PROFILE_SECTION_NAME \
            and profile_name not in cfg.sections():
            cfg.add_section(profile_name)
            cfg.write(fp)
        if not check_necessary_info_values(cfg, profile_name):
            for opt in NECESSARY_INFO:
                cfg.set(profile_name, opt, '')
            cfg.write(fp)
    return cfg

def get_profile(profile_name):
    cfg = get_raw_profile(profile_name)
    if not cfg.sections():
       section = DEFAULT_SECTION_NAME
    options = dict(cfg.items(section))
    Config = collections.namedtuple('Config', [m.upper() for m in six.iterkeys(options)])
    return Config._make(six.itervalues(options))




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


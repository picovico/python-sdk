import os
import errno
import itertools
import collections

import six

from . import PicovicoAPI
from .session import DEFAULT_DEVICE_ID
from .exceptions import PicovicoCLIError, PicovicoProfileError

NECESSARY_INFO = ('APP_ID', 'DEVICE_ID')
OPTIONAL_INFO_SECRET = ('APP_SECRET',)
OPTIONAL_INFO_USER = ('USERNAME',)
OPTIONAL_INFO_TOKEN = ('ACCESS_KEY', 'ACCESS_TOKEN')
DEFAULT_SECTION_NAME = six.moves.configparser.DEFAULTSECT
chained_info = itertools.chain(NECESSARY_INFO, OPTIONAL_INFO_SECRET, OPTIONAL_INFO_TOKEN, OPTIONAL_INFO_USER)
Profile = collections.namedtuple('Profile', itertools.chain(chained_info, ('PASSWORD', 'SECTION', 'AUTH')))


def get_config_file(dirname='.picovico', filename='profile.ini'):
    try:
        user_home = os.environ['HOME']
    except KeyError as e:
        raise PicovicoCLIError("Couldn't determine user home.")
    else:
        config_dir = os.path.join(user_home, dirname)
        try:
            os.makedirs(config_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e
        profile_file = os.path.join(config_dir, filename)
        return profile_file

def _has_configs_factory(cfg, section, err_message, err_code,
                            check_against=NECESSARY_INFO, check_against_more=None):
    if section != DEFAULT_SECTION_NAME and not cfg.has_section(section):
        raise PicovicoProfileError('No profile {}'.format(section), 10)
    all_checked = all(cfg.has_option(section, opt) for opt in check_against)
    if check_against_more:
        check_more = all(cfg.has_option(section, opt) for opt in check_against_more)
        all_checked = all_checked or check_more
    if all_checked:
        return True
    raise PicovicoProfileError(err_message, err_code)
    
def has_optional_configs(cfg, section=DEFAULT_SECTION_NAME,
                            both=True, username=False, token=False):
    err_message = """Seems like you have not authenticated or logged in.
                    Please do so."""
    config_args = {'check_against': OPTIONAL_INFO_SECRET}
    if username:
        config_args.update(check_against=OPTIONAL_INFO_USER)
    if token:
        config_args.update(check_against=OPTIONAL_INFO_TOKEN)
    if both:
        config_args.update(check_against=OPTIONAL_INFO_SECRET)
        config_args.update(check_against_more=OPTIONAL_INFO_USER)
    return _has_configs_factory(cfg, section, err_message, 5, **config_args)
        
def has_optional_username_configs(cfg, section=DEFAULT_SECTION_NAME):
    return has_optional_configs(cfg, section, username=True, both=False)

def has_optional_secret_configs(cfg, section=DEFAULT_SECTION_NAME):
    return has_optional_configs(cfg, section, both=False, username=False)

def has_optional_token_configs(cfg, section=DEFAULT_SECTION_NAME):
    return has_optional_configs(cfg, section, both=False, token=True)

def has_necessary_configs(cfg, section=DEFAULT_SECTION_NAME):
    err_message = 'Seems like you have not configured yet.'
    return _has_configs_factory(cfg, section, err_message, 0, check_against=NECESSARY_INFO)

def get_config(filename='profile.ini', section_name=DEFAULT_SECTION_NAME):
    profile_file = get_config_file(filename=filename)
    cfg = six.moves.configparser.SafeConfigParser()
    try:
        cfg.readfp(open(profile_file))
    except IOError:
        if section_name != DEFAULT_SECTION_NAME:
            cfg.add_section(section_name)
        #chain = itertools.chain(NECESSARY_INFO, OPTIONAL_INFO_SECRET, OPTIONAL_INFO_TOKEN, OPTIONAL_INFO_USER)
        for opt in NECESSARY_INFO:
            cfg.set(section_name, opt, '')
        cfg.write(open(profile_file, 'w'))
    else:
        has_necessary_configs(cfg, section_name)
    return cfg
    

def get_configure_profile(profile_name=None, auth=False, login=False):
    profile_info = {}
    profile_info.update({k: None for k in Profile._fields})
    profile_info.update(SECTION=profile_name or DEFAULT_SECTION_NAME) 
    profile_info['APP_ID'] = six.moves.input('Enter Application Id provided: ')
    assert profile_info['APP_ID'] and isinstance(profile_info['APP_ID'], six.string_types)
    profile_info['DEVICE_ID'] = six.moves.input('Enter Device Identifier->[default:{}]: '.format(DEFAULT_DEVICE_ID))
    if not profile_info['DEVICE_ID']:
        profile_info.update(DEVICE_ID=DEFAULT_DEVICE_ID)
    if auth and not login:
        profile_info['APP_SECRET'] = six.moves.input('Enter Application Secret: ')
        assert profile_info['APP_SECRET'] and isinstance(profile_info['APP_SECRET'], six.string_types)
    if login and not auth:
        profile_info['USERNAME'] = six.moves.input('Enter Picovico Username: ')
        assert profile_info['USERNAME']
        profile_info['PASSWORD'] = six.moves.input('Enter Picovico Password[Will not be stored]: ')
        assert profile_info['PASSWORD']
    if profile_info['APP_SECRET'] or (profile_info['USERNAME'] and profile_info['PASSWORD']):
        profile_info.update(AUTH=True)
    return Profile(**profile_info)
    
def set_configs(values_to_set, section_name=DEFAULT_SECTION_NAME, filename='profile.ini'):
    cfg = get_config(filename, section_name)
    for value in values_to_set:
        cfg.set(section_name, value.attr, str(value.value))
    cfg.write(open(filename, 'w'))

def read_config_values(section):
    cfg = get_config(section_name=section)
    if not cfg.sections():
        section = DEFAULT_SECTION_NAME
    options = dict(cfg.items(section))
    Config = collections.namedtuple('Config', [m.upper() for m in six.iterkeys(options)])
    return Config._make(six.itervalues(options))
    
def create_conf_values(list_of_values):
    Conf = collections.namedtuple('Conf', 'attr value')
    ret_val = []
    for val in list_of_values:
        ret_val.append(Conf._make(val))
    return ret_val

def write_access_info(profile_info):
    if profile_info.APP_SECRET:
        additional_conf = create_conf_values((('APP_SECRET', profile_info.APP_SECRET),))
    else:
        additional_conf = create_conf_values((('USERNAME', profile_info.USERNAME),))
    set_configs(additional_conf, section_name=profile_info.SECTION)
    api = PicovicoAPI(profile_info.APP_ID, profile_info.DEVICE_ID)
    if profile_info.APP_SECRET:
        api.authenticate(profile_info.APP_SECRET)
    else:
        api.login(profile_info.USERNAME, profile_info.PASSWORD)
    additional_conf = create_conf_values(((v, getattr(api, v.lower())) for v in OPTIONAL_INFO_TOKEN)) 
    set_configs(additional_conf, section_name=profile_info.SECTION)
    
def configure(profile_name, auth_with=None):
    key_args = {}
    if auth_with == 'login':
        key_args.update(login=True)
    elif auth_with == 'secret':
        key_args.update(auth=True)
    profile_info = get_configure_profile(profile_name, **key_args)
    necessary_conf = create_conf_values(((a, getattr(profile_info, a)) for a in NECESSARY_INFO))    
    set_configs(necessary_conf, section_name=profile_info.SECTION)
    if profile_info.AUTH:
        write_access_info(profile_info)
    
        
#def get_config_with_secret(profile_section='default'):
    #pass
    #cfg = get_config()
    #app_id = cfg.get('APP_ID')
#def get_config_with_token(profile_section='default'):
    #if not app_id:
        #raise PicovicoCLIError('No APP ID found.', code=0)
    #data = cfg.items(profile_section)
    

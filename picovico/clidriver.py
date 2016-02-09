import os
import errno

import six

from .session import PicovicoSessionMixin
from .exceptions import PicovicoCLIError, PicovicoProfileError

NECESSARY_INFO = ('APP_ID', 'DEVICE_ID')
OPTIONAL_INFO_SECRET = ('APP_SECRET',)
OPTIONAL_INFO_PASS = ('USERNAME', 'PASSWORD')

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
        #if os.path.isfile(profile_file):
            #return profile_file
        #os.make
        return profile_file

def _has_configs_factory(cfg, section, err_message, err_code,
                            check_against=NECESSARY_INFO, check_against_more=None):
    if section.upper() != six.moves.configparser.DEFAULTSECT and not cfg.has_section(section):
        raise PicovicoProfileError('No profile {}'.format(section), 10)
    all_checked = all(cfg.has_option(section, opt) for opt in check_against)
    if check_against_more:
        check_more = all(cfg.has_option(section, opt) for opt in check_against_more)
        all_checked = all_checked or check_more
    if all_checked:
        return True
    raise PicovicoProfileError(err_message, err_code)
    
def has_optional_configs(cfg, section=six.moves.configparser.DEFAULTSECT.lower(),
                            both=True, username=False):
    err_message = """Seems like you have not authenticated or logged in.
                    Please do so."""
    config_args = {'check_against': OPTIONAL_INFO_SECRET}
    if username:
        config_args.update(check_against=OPTIONAL_INFO_PASS)
    if both:
        config_args.update(check_against=OPTIONAL_INFO_SECRET)
        config_args.update(check_against_more=OPTIONAL_INFO_PASS)
    return _has_configs_factory(cfg, section, err_message, 5, **config_args)
        
def has_optional_username_configs(cfg, section=six.moves.configparser.DEFAULTSECT.lower()):
    return has_optional_configs(cfg, section, username=True, both=False)

def has_optional_secret_configs(cfg, section=six.moves.configparser.DEFAULTSECT.lower()):
    return has_optional_configs(cfg, section, both=False, username=False)

def has_necessary_configs(cfg, section=six.moves.configparser.DEFAULTSECT.lower()):
    err_message = 'Seems like you have not configured yet.'
    return _has_configs_factory(cfg, section, err_message, 0, check_against=NECESSARY_INFO)
    
def get_config(filename='profile.ini', section=six.moves.configparser.DEFAULTSECT.lower()):
        pass
        #cfg = six.moves.configparser.SafeConfigParser()
        #profile_file = get_config_file(filename)
        #if os.path.isfile(profile_file):
            #cfg.read(profile_file)
        #else:
        
        
        #else:
            #cfg.set('default', 'APP_ID')
            #with open(profile_file, 'wb') as f:
                #f.write(cfg)
            
        #//fp = open(profile_file, mode)
        #return cfg
        
def check_profiles(profile_section='default'):
    pass
    #cfg = get_config()
    #app_id = cfg.get('APP_ID')
    #if not app_id:
        #raise PicovicoCLIError('No APP ID found.', code=0)
    #data = cfg.items(profile_section)
    

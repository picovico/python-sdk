import os
import json
import errno

def get_user_directory_for_storage(dirname='.picovico'):
    try:
        user_home = os.environ['HOME']
    except KeyError as e:
        raise EnvironmentError("Couldn't determine user home.")
    else:
        config_dir = os.path.join(user_home, dirname)
        try:
            os.makedirs(config_dir)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e
        return config_dir

def get_file_from_storage(filename):
    config_dir = get_user_directory_for_storage()
    require_file = os.path.join(config_dir, filename)
    return require_file

def get_profile_file():
    return get_file_from_storage('profile.ini')

#def write_to_profile_file(profile_name, data):
    #pass
    
#def get_profile_file():
    #profile_file = get_profile_file()
    
def get_session_file():
    return get_file_from_storage('session')

def write_to_session_file(data):
    session_file = get_session_file()
    with open(session_file, 'wb') as f:
        json.dump(data, f)

def read_from_session_file():
    session_file = get_profile_file()
    data = None
    with open(session_file) as f:
        data = json.load(f)
    return data

#def check_file_exists()

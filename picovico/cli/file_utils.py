import os
import json
import errno

def get_user_directory_for_storage(dirname='.picovico'):
    user_home = os.environ.get('HOME', os.path.expanduser('~'))
    if not user_home:
        raise EnvironmentError("Couldn't determine user home.")
    config_dir = os.path.join(user_home, dirname)
    try:
        os.makedirs(config_dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise e
    return config_dir

def get_file_from_storage(filename):
    config_dir = get_user_directory_for_storage()
    return os.path.join(config_dir, filename)

def get_profile_file():
    return get_file_from_storage('profile.ini')

def has_profile_file():
    return os.path.isfile(get_profile_file())

def get_project_file():
    return get_file_from_storage('project')

def has_project_file():
    return os.path.isfile(get_project_file())

def get_session_file():
    return get_file_from_storage('session')

def has_session_file():
    return os.path.isfile(get_session_file())

def get_file_obj(filename, mode='rb'):
    try:
        return open(filename, mode)
    except IOError as e:
        if e.errno != errno.ENOENT:
            raise e
        return None

def write_json_data(filename, data):
    f = get_file_obj(filename, mode='wb')
    if f:
        with f:
            json.dump(data, f)

def write_to_session_file(data):
    session_file = get_session_file()
    write_json_data(session_file, data)

def write_to_project_file(data):
    project_file = get_project_file()
    write_json_data(project_file, data)

def delete_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)

def delete_session_file():
    session_file = get_session_file()
    delete_file(session_file)

def delete_project_file():
    project_file = get_project_file()
    delete_file(project_file)

def read_json_data(filename):
    data = None
    f = get_file_obj(filename)
    if f:
        with f:
            data = json.load(f)
    return data

def read_from_session_file():
    session_file = get_session_file()
    return read_json_data(session_file)

def read_from_project_file():
    project_file = get_project_file()
    return read_json_data(project_file)

def get_log_file(profile_name):
    return get_file_from_storage('picovico_{}_log'.format(profile_name.lower()))

import sys
import warnings
import json
import getpass
import six


DEFAULT_DEVICE_ID = 'com.pvcli.sdk'
VERSION = '2.1'
NO_PROFILE_MSG = 'No profile found. You should run configure.'

def pretty_print_result(result):
    six.print_(json.dumps(result, indent=2, sort_keys=True), file=sys.stdout)

def show_input(msg):
    return six.moves.input(msg)


def show_print(msg):
    six.print_("[*] "+msg, file=sys.stderr)


def show_warning(warn_text, stop=False):
    def pv_warning_format(message, category, filename, lineno, file=None, line=None):
        return '%s: %s' % (category.__name__, message)
    warnings.formatwarning = pv_warning_format
    warnings.warn(warn_text, UserWarning)
    if stop:
        sys.exit(0)


def generic_prompt(version=VERSION, profile_name=None):
    show_print('Picovico API [{}]'.format(version))
    if profile_name:
        show_print('Using Profile: {}'.format(profile_name))


def configure_prompt(version=VERSION):
    generic_prompt(version)
    text = '''You need to configure a profile to run picovico client.
    This will only save the configuration and not do any api call.

    Run:
        picovico-client configure

    See help for additional optional commands and arguments you can run
    with configure.'''
    show_print(text)
    return configure_necessary_info()

def retry_once_for_assertions(func, **kwargs):
    try:
        value = func(**kwargs)
    except AssertionError as e:
        show_warning(e.args[0]+'\n')
        value = func(**kwargs)
    return value

def configure_necessary_info():
    app_id = show_input('Enter Application Id provided: ')
    device_id = show_input('Enter Device Identifier->[default:{}]: '.format(DEFAULT_DEVICE_ID))
    assert app_id, 'Application ID is required'
    device_id = device_id or DEFAULT_DEVICE_ID
    return app_id, device_id


def password_save_query():
    show_warning('''Saving password may lead to exposure of password.
                    You can always enter password when required.\n''')
    save_password = show_input('Would You like to save password as well ?(Y or n)  ')
    yes_value = 'Yes'
    if save_password in (yes_value[0], yes_value[0].lower(),
                        yes_value.lower(), yes_value.upper(), yes_value):
        return configure_password_info()


def configure_password_info():
    password =  getpass.getpass('Enter Picovico Password: ')
    assert password, 'Password is required.'
    return password


def configure_login_info(coerce_password=False, query_password=True):
    username = show_input('Enter Picovico Username: ')
    password = None
    if query_password and not coerce_password:
        password = password_save_query()
    elif coerce_password and not query_password:
        password = configure_password_info()
    assert username, 'Username is required'
    return username, password


def configure_secret_info():
    app_secret = show_input('Enter Application Secret Provided: ')
    assert app_secret, 'Secret is required.'
    return app_secret


def show_action_result(action, result, profile_name):
    generic_prompt(profile_name=profile_name)
    show_print('Your Action: {}'.format(action))
    show_print('Result:')
    pretty_print_result(result)


def show_action_message(profile_name, message):
    generic_prompt(profile_name=profile_name)
    show_print(message)

def show_project_action_success(action, video_id, profile_name):
    msg = 'Your Project Action: {} was succesfully completed.'.format(action)
    msg += '\nYour current video is: {}'.format(video_id)
    show_action_message(profile_name, msg)

def show_action_success(action, profile_name):
    msg = 'Your Action: {} was succesfully completed.'.format(action)
    show_action_message(profile_name, msg)


def show_action_error(action, profile_name, status, message):
    error_names = {
        401: 'PicovicoUnAuthorized',
        404: 'PicovicoNotFound',
    }
    error_names.update({x: 'PicovicoServerError' for x in six.moves.range(500, 503)})
    error_name = error_names.get(status, 'PicovicoRequestError')
    msg = '{0}: {1}'.format(error_name, message)
    show_action_message(profile_name, msg)


def show_no_session(profile_name):
    msg = 'No session for profile: {}'.format(profile_name)
    msg += '\nEither login or authenticate this profile.'
    show_warning(msg, True)


def show_auth_login_msg(formatargs):
    msg = '''You are using {0} method but have {1} stored.
            Your {1} information will be deleted.'''
    show_warning(msg.format(*formatargs))

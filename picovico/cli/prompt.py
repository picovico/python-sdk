import warnings
import pprint

import six

DEFAULT_DEVICE_ID = 'com.pvcli.sdk'
VERSION = '2.5'

def show_input(msg):
    return six.moves.input(msg)

def show_print(msg):
    six.print_(msg)

def show_warning(warn_text):
    warnings.warn(warn_text)

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

# def show_results(data):

def configure_necessary_info():
    app_id = show_input('Enter Application Id provided: ')
    device_id = show_input('Enter Device Identifier->[default:{}]: '.format(DEFAULT_DEVICE_ID))
    assert app_id, 'Application ID is required'
    device_id = device_id or DEFAULT_DEVICE_ID
    return app_id, device_id

def password_save_query():
    show_warning('''Saving password may lead to exposure of password.
                    You can always enter password when required.''')
    save_password = show_input('Would You like to save password as well ?(Y or n)  ')
    yes_value = 'Yes'
    if save_password in (yes_value[0], yes_value[0].lower(), yes_value.lower(), yes_value.upper(), yes_value):
        return password_input_values()

def configure_password_info():
    password =  show_input('Enter Picovico Password: ')
    assert password, 'Password is required.'
    return password

def configure_login_info(coerce_password=False, query_password=True):
    username = show_input('Enter Picovico Username: ')
    if query_password and not coerce_password:
        password = password_save_query()
    elif coerce_password and not query_password:
        password = password_input_values()
    assert username, 'Username is required'
    return username, password

def configure_secret_info():
    app_secret = show_input('Enter Application Secret Provided: ')
    assert app_secret, 'Secret is required.'
    return app_secret

def show_action_result(action, result, profile_name):
    generic_prompt(profile_name)
    show_print('Your Action: {}'.format(action))
    show_print('Result:')
    show_print(pprint.pprint(result))

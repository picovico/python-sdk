import warnings

import six

DEFAULT_DEVICE_ID = 'com.pvcli.sdk'

def show_warning(warn_text):
    warnings.warn(warn_text)

def generic_prompt(version, profile_name):
    six.print_("Picovico API [{}]".format(version))
    six.print_("Using Profile: {}".format(profile_name))

def configure_prompt(version):
    generic_prompt(version)
    text = """You need to configure a profile to run picovico client.
    This will only save the configuration and not do any api call.

    Run:
        picovico-client configure

    See help for additional optional commands and arguments you can run
    with configure."""
    six.print_(text)

# def show_results(data):

def configure_input_values():
    app_id = six.moves.input('Enter Application Id provided: ')
    device_id = six.moves.input('Enter Device Identifier->[default:{}]: '.format(DEFAULT_DEVICE_ID)))
    assert app_id, 'Application ID is required'
    device_id = device_id or DEFAULT_DEVICE_ID
    return app_id, device_id

def password_save_query()
    save_password = six.moves.input('Would You like to save password as well ?(Y or n)  ')
    yes_value = 'Yes'
    if save_password in (yes_value[0], yes_value[0].lower(), yes_value.lower(), yes_value.upper(), yes_value):
        return password_input_values()

def password_input_value()
    password =  six.moves.input('Enter Picovico Password: ')
    assert password, 'Password is required.'
    return password

def login_input_value(coerce_password=False, query_password=True):
    username = six.moves.input('Enter Picovico Username: ')
    if query_password and not coerce_password:
        password = password_save_query()
    elif coerce_password and not query_password:
        password = password_input_values()
    assert username, 'Username is required'
    return username, password

def secret_input_value():
    app_secret = six.moves.input('Enter Application Secret Provided: ')
    assert app_secret, 'Secret is required.'
    return app_secret

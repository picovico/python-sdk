import warnings

import six

def show_warning(warn_text):
    warnings.warn(warn_text)

def generic_prompt(version):
    six.print_("Picovico API [{}]".format(version))

def need_configure(version):
    generic_prompt(version)
    text = """You need to configure a profile to run picovico client.
    This will only save the configuration and not do any api call.
    
    Run:
        picovico-client configure
    
    See help for additional optional commands and arguments you can run
    with configure."""
    six.print_(text)

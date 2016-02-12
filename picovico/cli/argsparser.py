import argparse
import re
import itertools

import six

from . import cli_actions as actions
from ..components.base import PicovicoBaseComponent
#class PicovicoConfigureAction(argparse.Action):

comp_re = re.compile(r'^(get|delete)_([a-z]+)$')

#class PicovicoArgumentParser(argparse.ArgumentParser):
    #def __init__()
parser = argparse.ArgumentParser(prog='picovico-client')
for action in actions.all_actions:
    parser.add_argument(action, nargs='?')
    if action == 'configure':
        sub = parser.add_subparsers(dest=action)
        conf_login = sub.add_parser('login')
        conf_login.add_argument('login')
        conf_auth = sub.add_parser('authenticate')
        conf_login.add_argument('authenticate')
    if action not in six.iterkeys(actions.prompt_actions):
        comp = comp_re.search(action)
        if action not in itertools.chain(actions.exempt_actions, actions.exempt_id_actions):
            if comp and comp.group(2) in PicovicoBaseComponent._components[1:]:
                comp_name = comp.group(2)
                sub = parser.add_subparsers(dest=action)
                #comp_parser = sub.add_parser(comp_name)
parser.add_argument('-p', '--profile', type=str)

#configure_group = parser.add_argument_group('configure', "Configure the client with credentials.")
#configure_group.add_argument('login', nargs='?', help='login help')
#configure_group.add_argument('auth', nargs='?', help='authenticate help')


if __name__ == '__main__':
    parser.parse_args()

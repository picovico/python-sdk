# from __future__ import absolute_import
import argparse

from . import driver as cli_driver

def get_parser():
    actions = cli_driver.get_cli_commands()
    parser = argparse.ArgumentParser(prog='picovico-client')
    sub_parser = parser.add_subparsers(title='subcommands')
    for action in actions:
        sub = sub_parser.add_parser(action.COMMAND,  help='{} help'.format(action.COMMAND))
        sub.add_argument('--profile', nargs=1, type=str)
        if action.OPTIONS:
            for option in action.OPTIONS:
                name = option.pop('name')
                sub.add_argument(name, **option)
    return parser

def picovico_parse_args():
    parser = get_parser()
    import sys
    if sys.argv and len(sys.argv) > 1:
        action = sys.argv[1]
    ns = parser.parse_args()
    arguments = ns.__dict__.copy()
    arguments.pop('profile')
    if len(arguments) and 'include' not in arguments:
        arguments = {k: v for k, v in arguments.items()}
    elif 'include' in arguments:
        arguments.pop('include')
        if ns.include:
            arguments.update({ns.include: True})
    if ns.profile:
        ns.profile = ns.profile[0]
    cli_driver.call_api_actions(action, ns.profile, **arguments)

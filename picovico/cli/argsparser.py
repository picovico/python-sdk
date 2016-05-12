# from __future__ import absolute_import
import argparse

import six

from picovico.cli import driver as cli_driver

help_usage = """ Picovico SDK client utility. 
                ------------------------------

picovico-client action args

    Actions:
        configure
        login
        logout
        authenticate
        get-{component}s music, photo, style, video
        project
    
    Project Actions:
        define
        begin
        close
        render
        preview
        duplicate
        save
"""

def create_arguments(parser, actions):
    for action in actions:
        name = action.pop('name')
        parser.add_argument(name, **action)

def create_subcommands(parser, actions, sub_title, sub_dest, **extras):
    sub_parser = parser.add_subparsers(title=sub_title, dest=sub_dest)
    for action in actions:
        sub = sub_parser.add_parser(action.COMMAND,  help='{} help'.format(action.COMMAND))
        #if hasattr(action, 'GROUPS') and action.GROUPS:
            #groups = sub.add_argument_group(action.GROUP_NAME)
            #create_arguments(groups, action.GROUPS)
        if hasattr(action, 'OPTIONS') and action.OPTIONS:
            create_arguments(sub, action.OPTIONS)
        for k, v in six.iteritems(extras):
            sub.add_argument(k, **v)
        if hasattr(action, 'SUBCOMMANDS') and action.SUBCOMMANDS:
            sub_parser = create_subcommands(sub, action.SUBCOMMANDS, action.SUB_TITLE, action.SUB_DEST, **action.SUB_EXTRAS)
    return parser

def get_parser():
    actions = cli_driver.get_cli_commands()
    parser = argparse.ArgumentParser(prog='picovico-client', description=help_usage, formatter_class=argparse.RawTextHelpFormatter)
    profile_args = {
        '--profile': {'type': str}
    }
    parser = create_subcommands(parser, actions, 'subcommand', 'action', **profile_args)
    return parser

def picovico_parse_args():
    parser = get_parser()
    ns = parser.parse_args()
    arguments = ns.__dict__.copy()
    #if len(arguments) and 'include' not in arguments:
        #arguments = {k.replace('-', '_'): v for k, v in arguments.items()}
    #el
    if 'include' in arguments:
        arguments.pop('include')
        if ns.include:
            arguments.update({ns.include: True})
    #print arguments
    cli_driver.call_api_actions(**arguments)

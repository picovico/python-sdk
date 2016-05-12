import sys

import pytest

from picovico.cli.driver import get_cli_commands
from picovico.cli.argsparser import get_parser, picovico_parse_args

parser = get_parser()

def add_profile_command(command, append_list, profile_name):
    append_list.append(command+' --profile '+profile_name)

def get_command_strings(command, append_list, profile_name):
    com = 'picovico-client '+command.COMMAND
    append_list.append(com)
    add_profile_command(com, append_list, profile_name)
    if command.OPTIONS:
        for opt in command.OPTIONS:
            opt_com = com+' '+opt.get('name')
            if 'choices' in opt:
                for choice in opt['choices']:
                    choice_com = opt_com+' '+choice
                    append_list.append(choice_com)
                    add_profile_command(choice_com, append_list, profile_name)
            else:
                append_list.append(opt_com)
                add_profile_command(opt_com, append_list, profile_name)


def get_configure_commands():
    commands = []
    for command in get_cli_commands():
        if command.COMMAND == 'configure':
            get_command_strings(command, commands, 'SOME')
            additional_commands = [com+' --log' for com in commands if '--include' in com]
            commands.extend(additional_commands)
    return commands

def get_all_commands():
    commands = []
    for command in get_cli_commands():
        if command.COMMAND != 'project':
            get_command_strings(command, commands, 'SOME')
    return commands
    #profile = 'SOME'
    #command = 'configure'
    #command_log = 'configure --log'
    #command_profile = command+' --profile '+profile
    #command_profile_log = command+' --profile '+profile
    #command_include_login = command + ' --include login'
    #command_include_authenticate = command + ' --include authenticate'
    #command_include_login_log = command_log + ' --include login'
    #command_include_login = command + ' --include authenticate'

class TestPVCLIArgs:
    #@pytest.mark.parametrize('command', get_configure_commands())
    #def test_parser_configure_commands(self, command):
        #ns = parser.parse_args(command.split())
        #if 'include' in command:
            #assert ns.include
        #if 'profile' in command:
            #assert ns.profile

    @pytest.mark.parametrize('command', get_configure_commands())
    def test_picovico_configure(self, mocker, command):
        def side_effect(*args, **kwargs):
            assert kwargs['action'] == 'configure'
            assert 'log' in kwargs and kwargs['log'] in (True, False)
            assert 'profile' in kwargs and kwargs['profile'] in (None, 'SOME')
        mock_sys = mocker.patch.object(sys, 'argv', command.split())
        mock_call_api_action = mocker.patch('picovico.cli.argsparser.pv_cli_driver.call_api_actions')
        mock_call_api_action.side_effect = side_effect
        picovico_parse_args()
        # mock_sys = mocker.patch.object(sys, 'argv', command.split()+['photo'])
        # with pytest.raises(SystemExit):
            # picovico_parse_args()

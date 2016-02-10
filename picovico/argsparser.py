import argparse

#import six

#class PicovicoConfigureAction(argparse.Action):

            

#class PicovicoArgumentParser(argparse.ArgumentParser):
    #def __init__()
parser = argparse.ArgumentParser(prog='picovico-client')
parser.add_argument('configure', nargs='?', help='configure help')
parser.add_argument('-p', '--profile', help='profile help', type=str)
configure_group = parser.add_argument_group('configure', "Configure the client with credentials.")
configure_group.add_argument('login', nargs='?', help='login help')
configure_group.add_argument('auth', nargs='?', help='authenticate help')


if __name__ == '__main__':
    parser.parse_args()

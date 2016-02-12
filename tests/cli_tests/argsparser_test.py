from picovico.cli.argsparser import parser

parse = parser.parse_args

class TestPVCLIArgs:
    def test_args_functionality(self):
        parser.print_help()

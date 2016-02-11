from picovico.argsparser import parser

parse = parser.parse_args

class TestPVCLIArgs:
    def test_args_functionality(self):
        res = parse(['configure'])

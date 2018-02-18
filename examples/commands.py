#!/usr/bin/env python
import nicfit

@nicfit.Command.register
class Hi(nicfit.Command):
    NAME = "hi"
    ALIAS = ["hello"]
    HELP = "A simple hello command."
    DESC = "This command can speak Spanish a command line option."

    def _initArgParser(self, parser):
        parser.add_argument("--spanish", action="store_true",
                            help="Respond in Spanish")

    def _run(self):
        print("Hola" if self.args.spanish else "Hi")

@nicfit.Command.register
class bye(nicfit.Command):
    HELP = "A simple hello command."
    def _run(self):
        print("Bye")

# Until Python 3.7 ArgumentParser.add_subparsers does not support the `required`
# keyword, nicfit.ArgumentParser handles this.
parser = nicfit.ArgumentParser()
nicfit.Command.loadCommandMap(parser.add_subparsers(dest="cmd", required=True))
args = parser.parse_args()
args.command_func(args)

"""
$ ./cmds2.py 
usage: cmds2.py [-h] {bye,hi} ...
cmds2.py: error: the following arguments are required: cmd
$ ./cmds2.py --help
usage: cmds2.py [-h] {hi,bye} ...

positional arguments:
  {hi,bye}
    hi        A simple hello command.
    bye       A simple hello command.

optional arguments:
  -h, --help  show this help message and exit
$ ./cmds2.py hi --help
usage: cmds2.py hi [-h] [--spanish]

This command can speak Spanish a command line option.

optional arguments:
  -h, --help  show this help message and exit
  --spanish   Respond in Spanish
$ ./cmds2.py hi --spanish
Hola
"""

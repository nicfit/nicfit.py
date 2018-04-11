#!/usr/bin/env python
import nicfit

@nicfit.Command.register
class cmd1(nicfit.Command):
    def _run(self):
        print("cmd1:", self.args)


@nicfit.Command.register
class cmd2(nicfit.Command):
    def _run(self):
        print("cmd2:", self.args)


@nicfit.Command.register
class cmd3(nicfit.command.SubCommandCommand):
    class sub1(nicfit.Command):
        def _initArgParser(self, parser):
            parser.add_argument("-o")
            parser.add_argument("-p")

        def _run(self):
            print("cmd3 sub1:", self.args)

    class sub2(nicfit.Command):
        def _initArgParser(self, parser):
            parser.add_argument("--option1")
            parser.add_argument("--option2", action="store_true")

        def _run(self):
            print("cmd3 sub2:", self.args)

    SUB_CMDS = [sub1, sub2]


# Until Python 3.7 ArgumentParser.add_subparsers does not support the `required`
# keyword, nicfit.ArgumentParser handles this.
parser = nicfit.ArgumentParser()
commands = nicfit.Command.loadCommandMap(parser.add_subparsers(dest="cmd", required=False))

args = parser.parse_args()
if args.cmd:
    args.command_func(args)
else:
    print("No command")

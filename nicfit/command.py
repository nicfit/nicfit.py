# -*- coding: utf-8 -*-
from collections import OrderedDict
from ._argparse import ArgumentParser


def register(CommandSubClass):
    """A class decorator for Command classes to register in the default set."""
    name = CommandSubClass.name()
    if name in Command._all_commands:
        raise ValueError("Command already exists: " + name)
    Command._all_commands[name] = CommandSubClass
    return CommandSubClass


class CommandError(Exception):
    """Base error type for nicfit.command.Command errors."""
    def __init__(self, msg, exit_status=1):
        super().__init__(msg)
        self.exit_status = exit_status


class Command(object):
    """Base class for commands."""
    _all_commands = OrderedDict()
    register = register

    @classmethod
    def name(Class):
        return Class.NAME if hasattr(Class, "NAME") else Class.__name__

    @classmethod
    def help(Class):
        return Class.HELP if hasattr(Class, "HELP") else None

    @classmethod
    def desc(Class):
        return Class.DESC if hasattr(Class, "DESC") else Class.help()

    @classmethod
    def aliases(Class):
        return Class.ALIASES if hasattr(Class, "ALIASES") else []

    def __init__(self, subparsers=None):
        self.subparsers = subparsers
        if subparsers:
            self.parser = self.subparsers.add_parser(self.name(),
                                                     help=self.help(),
                                                     description=self.desc(),
                                                     aliases=self.aliases())
        else:
            self.parser = ArgumentParser(prog=self.name(),
                                         description=self.desc(),
                                         epilog=self.help())
        self.parser.set_defaults(command_func=self.run)
        self._initArgParser(self.parser)

    def _initArgParser(self, parser):
        pass

    def run(self, args):
        self.args = args
        return self._run()

    def _run(self):
        raise NotImplementedError("Must implement a _run function")

    # TODO: deprecate me
    @staticmethod
    def initAll(subparsers=None):
        if not Command._all_commands:
            raise ValueError("No commands have been registered")

        cmds = []
        for Cmd in Command._all_commands.values():
            cmds.append(Cmd(subparsers))
        return cmds

    @classmethod
    def iterCommands(Class):
        return iter(Class._all_commands.values())


__all__ = ["register", "CommandError", "Command"]

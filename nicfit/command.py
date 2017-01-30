# -*- coding: utf-8 -*-
from collections import OrderedDict


def register(CommandSubClass):
    """A class decorator for Command classes to register in the default set."""
    Command._all_commands[CommandSubClass.name()] = CommandSubClass
    return CommandSubClass


class CommandError(Exception):
    """Base error type for nicfit.command.Command errors."""
    def __init__(self, msg, exit_status=1):
        super().__init__(msg)
        self.exit_status = exit_status


class Command(object):
    """Base class for commands."""
    _all_commands = OrderedDict()

    @classmethod
    def name(Class):
        return Class.NAME if hasattr(Class, "NAME") else Class.__name__

    @classmethod
    def help(Class):
        return Class.HELP if hasattr(Class, "HELP") else None

    def __init__(self, subparsers):
        self.subparsers = subparsers
        self.parser = self.subparsers.add_parser(self.name(), help=self.help())
        self._initArgParser(self.parser)
        self.parser.set_defaults(command_func=self.run)

    def _initArgParser(self, parser):
        pass

    def run(self, args):
        self.args = args
        return self._run()

    def _run(self):
        raise NotImplementedError("Must implement a _run function")

    @staticmethod
    def initAll(subparsers):
        for cmd in Command._all_commands.values():
            cmd(subparsers)
        else:
            raise ValueError("No commands have been registered")


__all__ = ["register", "CommandError", "Command"]

# -*- coding: utf-8 -*-
from collections import OrderedDict
from ._argparse import ArgumentParser


def register(CommandSubClass):
    """A class decorator for Command classes to register in the default set."""
    name = CommandSubClass.name()
    # FIXME: check for alias collisions
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

    def __init__(self, subparsers=None, **kwargs):
        """Construct a command.
        Any `kwargs` are added to the class object using ``setattr``.
        All commands have an ArgumentParser, either constructed here or when
        ``subparsers`` is given a new parser is created using its ``add_parser``
        method.
        """
        for name, value in kwargs.items():
            setattr(self, name, value)

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


class AsyncCommand(Command):
    async def run(self, args):
        self.args = args
        return await self._run()

    async def _run(self):
        raise NotImplementedError("Must implement a _run function")


class SubCommandCommand(Command):
    """Like a normal command, but structured as a command with sub-commands,
    each with its own argument interface (and argument parser).
    """
    SUB_CMDS = []
    DEFAULT_CMD = None

    def __init__(self, *args, **kwargs):
        self._sub_cmds = []
        self._ctor_kwargs = kwargs
        super().__init__(*args, **kwargs)

    def _run(self):
        try:
            self.args.arg0 = self.args.argv[1]
        except IndexError:
            self.args.arg0 = ""
        return self.args.command_func(self.args)

    def _initArgParser(self, parser):
        def_cmd = None
        subparsers = parser.add_subparsers(title="Sub-commands",
                                           dest="command", prog=self.name())
        subparsers.required = self.DEFAULT_CMD is None
        for CmdClass in self.SUB_CMDS:
            cmd = CmdClass(subparsers=subparsers, **self._ctor_kwargs)
            if CmdClass is self.DEFAULT_CMD:
                def_cmd = cmd
            self._sub_cmds.append(cmd)
        parser.set_defaults(command_func=def_cmd.run if def_cmd else None)


class AsyncSubCommandCommand(SubCommandCommand):
    async def run(self, args):
        self.args = args
        return await self._run()

    async def _run(self):
        try:
            self.args.arg0 = self.args.argv[1]
        except IndexError:
            self.args.arg0 = ""
        return await self.args.command_func(self.args)


__all__ = ["register", "CommandError", "Command", "SubCommandCommand",
           "AsyncCommand", "AsyncSubCommandCommand"]

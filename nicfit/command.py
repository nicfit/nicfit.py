import functools
from collections import OrderedDict, defaultdict
from deprecation import deprecated
from .__about__ import __version__
from ._argparse import ArgumentParser


@deprecated(deprecated_in="0.8", removed_in="0.9", current_version=__version__,
            details="Use the static class methods from nicfit.command.Command "
                    "or subclass thereof.")
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


class Command:
    """Base class for commands."""
    # XXX: deprectated, with with global register
    _all_commands = OrderedDict()

    # Using partial so subclasses can use as a builder.
    CommandDict = functools.partial(defaultdict, OrderedDict)
    _registered_commands = CommandDict()

    @classmethod
    def register(Class, CommandSubClass):
        """A class decorator for Command classes to register."""
        for name in [CommandSubClass.name()] + CommandSubClass.aliases():
            if name in Class._registered_commands[Class]:
                raise ValueError("Command already exists: " + name)
            Class._registered_commands[Class][name] = CommandSubClass
        return CommandSubClass

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
    @deprecated(deprecated_in="0.8", removed_in="0.9",
                details="Use :meth:`Command.loadCommandMap` instead.",
                current_version=__version__)
    def initAll(subparsers=None):
        if not Command._all_commands:
            raise ValueError("No commands have been registered")

        seen = set()
        cmds = []
        for Cmd in Command._all_commands.values():
            if Cmd not in seen:
                cmds.append(Cmd(subparsers))
                seen.add(Cmd)
        return cmds

    @classmethod
    @deprecated(deprecated_in="0.8", removed_in="0.9",
                details="Use :meth:`Command.loadCommandMap.values()` instead.",
                current_version=__version__)
    def iterCommands(Class):
        return iter(set(Class._all_commands.values()))

    @classmethod
    def loadCommandMap(Class, subparsers=None, instantiate=True, **cmd_kwargs):
        """Instantiate each registered command to a dict mapping name/alias to
        instance.

        Due to aliases, the returned length may be greater there the number of
        commands, but the unique instance count will match.
        """
        if not Class._registered_commands:
            raise ValueError("No commands have been registered with {}"
                             .format(Class))

        all = {}
        for Cmd in set(Class._registered_commands[Class].values()):
            cmd = Cmd(subparsers=subparsers, **cmd_kwargs) \
                        if instantiate else Cmd
            for name in [Cmd.name()] + Cmd.aliases():
                all[name] = cmd
        return all


class SubCommandCommand(Command):
    """Like a normal command, but structured as a command with sub-commands,
    each with its own argument interface (and argument parser).
    """
    SUB_CMDS = []
    DEFAULT_CMD = None

    def __init__(self, title="Sub-commands", subparsers=None, **kwargs):
        self.title = title
        self._sub_cmds = []
        self._ctor_kwargs = dict(kwargs)
        super().__init__(subparsers=subparsers)

    def _run(self):
        return self.args.command_func(self.args)

    def _initArgParser(self, parser):
        def_cmd = None
        subparsers = parser.add_subparsers(title=self.title, dest="command",
                                           prog=self.name(),
                                           required=not self.DEFAULT_CMD)
        for CmdClass in self.SUB_CMDS:
            cmd = CmdClass(subparsers=subparsers, **self._ctor_kwargs)
            if CmdClass is self.DEFAULT_CMD:
                def_cmd = cmd
            self._sub_cmds.append(cmd)
        parser.set_defaults(command_func=def_cmd.run if def_cmd else None)


__all__ = ["register", "CommandError", "Command", "SubCommandCommand"]

import re
import uuid

from ..command import Command as _BaseCommand
from ..command import SubCommandCommand as _SubCommandCommand
from ..aio import Command as _BaseAsyncCommand
from ..aio import SubCommandCommand as _BaseAsyncSubCommandCommand
from .completion import _updateCompleterDict, WordCompleter


class _CommandCompleterMixin:
    def _cmdRegex(self, cmd_grp=None):
        """Get command regex string and completer dict."""
        cmd_grp = cmd_grp or "cmd"
        help_opts = ("-h", "--help")

        cmd = self.name()
        names = "|".join([re.escape(cmd)] +
                         [re.escape(a) for a in self.aliases()])

        opts = []
        for action in self.parser._actions:
            opts += [a for a in action.option_strings
                        if a not in help_opts]

        opts_re = "|".join([re.escape(o) for o in opts])
        if opts_re:
            opts_re = rf"(\s+(?P<{cmd_grp}_opts>{opts_re}))*"

        help_re = "|".join([re.escape(o) for o in help_opts])
        help_re = rf"(\s+(?P<HELP_OPTS>{help_re}))*"

        completers = {}
        if opts_re:
            completers[f"{cmd_grp}_opts"] = WordCompleter(opts)
        # Singe Help completer added elsewhere

        return tuple([
            rf"""(?P<{cmd_grp}>{names}){opts_re}{help_re}""",
            completers
        ])

    def grammar(self, completers: dict):
        regex, new_completers = self._cmdRegex()
        regex = _updateCompleterDict(completers, new_completers, regex)
        return rf"(\s* {regex} \s*)"


class _SubCommandCompleterMixin(_CommandCompleterMixin):
    def _cmdRegex(self, cmd_grp=None):
        regex, completers = super()._cmdRegex(cmd_grp=cmd_grp)

        sub_grammars = []
        sub_cmds = []
        group_name = f"{self.name()}_subcmd"
        for sub in self._sub_cmds:
            sub_regex, sub_completers = sub._cmdRegex(cmd_grp=group_name)
            sub_regex = _updateCompleterDict(completers, sub_completers,
                                             sub_regex)
            sub_grammars.append(rf"(\s* {sub_regex} \s*)")
            sub_cmds += [sub.name()] + sub.aliases()

        sub_grammars = " |\n".join(sub_grammars)
        regex = rf"""{regex} ( {sub_grammars} )"""
        _updateCompleterDict(completers, {group_name: WordCompleter(sub_cmds)})

        return regex, completers

    def grammar(self, completers: dict):
        regex, new_completers = self._cmdRegex()
        regex = _updateCompleterDict(completers, new_completers, regex)
        return rf"(\s* {regex} \s*)"


class Command(_BaseCommand, _CommandCompleterMixin):
    pass


class SubCommandCommand(_SubCommandCommand, _SubCommandCompleterMixin):
    pass


# Async command interfaces
class async:
    class Command(_BaseAsyncCommand, _CommandCompleterMixin):
        pass

    class SubCommandCommand(_BaseAsyncSubCommandCommand,
                            _SubCommandCompleterMixin):
        pass


class _Namer:
    def __init__(self):
        self._names = set()
        self._counter = 0

    def get(self, name):
        if name not in self._names:
            self._names.add(name)
            return name

        n = f"{name}_{self._counter + 1}"
        if n not in self._names:
            self._counter += 1
            self._names.add(n)
            return n

        return f"{name}_{uuid.uuid4()}"

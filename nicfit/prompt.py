import re
import uuid
from prompt_toolkit.contrib.completers import WordCompleter

from .command import Command as _BaseCommand
from .aio import Command as _BaseAsyncCommand
from .command import SubCommandCommand as _SubCommandCommand
from .aio import SubCommandCommand as _BaseAsyncSubCommandCommand


class _CommandCompleterMixin:
    def _cmdRegex(self):
        """Get command regex string and completer dict."""
        cmd = self.name()
        names = "|".join([re.escape(cmd)] +
                         [re.escape(a) for a in self.aliases()])
        opts = []
        for action in self.parser._actions:
            opts += [a for a in action.option_strings]
        opts_re = "|".join([re.escape(o) for o in opts])

        return (f"(?P<cmd>{names}) \s+ (?P<{cmd}_opts>{opts_re})*",
                {f"{cmd}_opts": WordCompleter(opts)})

    def grammar(self):
        # TODO: Have a single -h/--help WordCompleter and reuse
        regex, completers = self._cmdRegex()
        return (rf"(\s* {regex} \s*)", completers)

    @staticmethod
    def updateCompleterDict(completers, cdict, regex=None):
        """Merges ``cdict`` into ``completers``. In the event that a key
        in cdict already exists in the completers dict a ValueError is raised
        iff ``regex`` false'y. If a regex str is provided it and the duplicate
        key are updated to be unique, and the updated regex is returned.
        """
        for key in cdict:
            if key in completers and not regex:
                raise ValueError(f"Duplicate completion key: {key}")
            elif key in completers:
                uniq = "_".join([key, str(uuid.uuid4()).replace("-","")])
                regex = regex.replace(f"P<{key}>", f"P<{uniq}>")
                completers[uniq] = cdict[key]
            else:
                completers[key] = cdict[key]

        return regex


class _SubCommandCompleterMixin:
    def grammar(self):
        '''
        regex, completers = self._cmdRegex()

        grammars = []
        completers = {}
        subcmd_words = []
        for cmd in self._sub_cmds:
            subcmd_words += [cmd.name()] + cmd.aliases()
            g, c = cmd._cmdRegex()
            g = g.replace("?P<cmd>", f"?P<{self.name()}_subcmd>")
            g = self.updateCompleterDict(completers, c, g)
            grammars.append(rf"(\s* {regex} \s+ {g} \s*)")

        return "|\n".join(grammars), completers
        '''
        # FIXME: ^^^^ WIP, disabled because base commands are not yet solid..
        # FIXME: and not complicating the massive regex until ready
        return "", {}


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

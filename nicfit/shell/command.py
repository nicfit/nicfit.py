import re
import textwrap
import operator

from prompt_toolkit.token import Token
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.shortcuts import print_tokens

from ..command import Command as _BaseCommand
from ..command import SubCommandCommand as _SubCommandCommand
from ..aio import Command as _BaseAsyncCommand
from ..aio import SubCommandCommand as _BaseAsyncSubCommandCommand
from .completion import _updateCompleterDict, WordCompleter
from . import output


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


class _HelpCommanMixin:
    NAME = "help"
    HELP_STYLE = {**output.Styles.DEFN_LIST_DICT,
                  **{Token.Name: "bold italic"}}
    _help_style = style_from_dict(HELP_STYLE)
    ALIASES = ["?", "??"]
    DESC = "Display a list of commands. Invoke command with -h/--help for " \
           "more info."
    COMMAND_CLASS = None

    def _initArgParser(self, parser):
        parser.add_argument("-l", "--long", action="store_true",
                            help="Display command descriptions in listing. "
                                 "Use the alias ?? to achieve the same.")

    def _run(self):
        def isLongForm():
            return (self.args.long or self.args.arg0 == "??")

        listing = []
        seen_cmds = set()
        for c in set(self.COMMAND_CLASS.loadCommandMap(instantiate=False)
                         .values()):
            if c not in seen_cmds:
                listing.append((c.name(), c.aliases(),
                                c.desc() if isLongForm() else ""))
                seen_cmds.add(c)

        tokens = []
        indent = " " * 2
        for cmd, aliases, desc in sorted(listing,
                                         key=operator.itemgetter(0)):
            alias_toks = []
            if aliases:
                alias_toks = [
                    (Token.Delim, "\t["),
                    (Token, f"alias{'es' if len(aliases) > 1 else ''}: "),
                    (Token.Name, ",".join(aliases)),
                    (Token.Delim, "]"),
                ]
            tokens += [(Token.Name, cmd)] + alias_toks + \
                      [(Token.Delim, "\n" if desc else ""),
                       (Token, indent if desc else ""),
                       (Token.Definition,
                        textwrap.fill(desc or "", width=70,
                                      initial_indent=indent,
                                      subsequent_indent=indent)),
                       (Token, "\n"),
                       ]

        if isLongForm():
            output.printTitle("\nAll Commands")
        print_tokens(tokens, style=self._help_style)


class HelpCommand(_HelpCommanMixin, Command):
    pass


# Async command interfaces
class aio:
    class Command(_BaseAsyncCommand, _CommandCompleterMixin):
        pass

    class SubCommandCommand(_BaseAsyncSubCommandCommand,
                            _SubCommandCompleterMixin):
        pass

    class HelpCommand(_HelpCommanMixin, _BaseAsyncSubCommandCommand):
        async def _run(self):
            return super()._run()

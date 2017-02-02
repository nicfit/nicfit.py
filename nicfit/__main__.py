# -*- coding: utf-8 -*-
from pathlib import Path
import nicfit
from . import version
from .console import ansi
from .console.ansi import Fg, Style

try:
    from cookiecutter.main import cookiecutter
    from cookiecutter.exceptions import CookiecutterException
    import click.exceptions
except ImportError:  # pragma: nocover
    cookiecutter = None


@nicfit.command.register
class CookieCutter(nicfit.Command):
    NAME = "cookiecutter"
    HELP = "Create a nicfit.py Python project skeleton."

    def _initArgParser(self, parser):
        parser.add_argument("outdir", metavar="PATH",
            help="Where to output the generated project dir into")
        parser.add_argument("--config-file", metavar="PATH",
                            help="User configuration file", default=None)
        parser.add_argument("--no-input", action="store_true",
                            help="Do not prompt for parameters and only use "
                                 "cookiecutter.json file content")

    def _run(self):
        if cookiecutter is None:
            print("CookieCutter not installed: pip install cookiecutter")
            return 1

        template_d = None
        for p in [Path(__file__).parent / "cookiecutter",
                  Path(__file__).parent.parent / "cookiecutter",
                 ]:
            if p.exists():
                template_d = p
                break
        assert template_d
        try:
            cookiecutter(str(template_d), config_file=self.args.config_file,
                         no_input=self.args.no_input, overwrite_if_exists=True,
                         output_dir=self.args.outdir)
        except click.exceptions.Abort as ex:
            raise KeyboardInterrupt()  # pragma: nocover
        except CookiecutterException as ex:
            exstr = str(ex)
            print("CookieCutter error: {}"
                  .format(exstr if exstr else ex.__class__))
            return 1


class Nicfit(nicfit.Application):
    def __init__(self):
        super().__init__(version=version)
        subs = self.arg_parser.add_subparsers(title="Commands",
                                              add_help_subcmd=True,
                                              dest="command")
        nicfit.Command.initAll(subs)

    def _main(self, args):
        ansi.init()
        if args.command:
            return args.command_func(args)
        else:
            print(Fg.red("\m/ {} \m/".format(Style.inverse("Slayer"))))


app = Nicfit()
if __name__ == "__main__":
    app.run()  # pragma: nocover

# -*- coding: utf-8 -*-
import os
import shutil
import subprocess
from uuid import uuid4
from hashlib import md5
from pathlib import Path

import nicfit
from . import version
from .util import copytree
from .console import ansi, perr, pout
from .console.ansi import Fg, Style

try:
    from cookiecutter.main import cookiecutter
    from cookiecutter.exceptions import CookiecutterException
    import click.exceptions
except ImportError:  # pragma: nocover
    cookiecutter = None

HASH_FILE = Path("./.cookiecutter.md5")


@nicfit.command.register
class CookieCutter(nicfit.Command):
    NAME = "cookiecutter"
    HELP = "Create a nicfit.py Python project skeleton."
    OLD_CC_USER_CONFIG = ".cookiecutter.json"
    CC_USER_CONFIG = ".cookiecutter.yml"
    ALIASES = ["cc"]

    def _initArgParser(self, parser):
        parser.add_argument("outdir", metavar="PATH",
            help="Where to output the generated project dir into")
        parser.add_argument("--config-file", metavar="PATH",
                            help="User configuration file", default=None)
        parser.add_argument("--no-input", action="store_true",
                            help="Do not prompt for parameters and only use "
                                 "{} file content".format(self.CC_USER_CONFIG))
        parser.add_argument("--no-config", action="store_true",
                            help="Use no user config (overrides --config_file)")
        parser.add_argument("--no-clone", action="store_true",
                            help="Do not clone a local repo if one is found.")
        parser.add_argument("--merge", action="store_true",
                            help="Merge CookieCutter output against local "
                            "repository (if found). Ignored when used "
                            "with --no-clone")
        parser.add_argument("--ignore-md5s", action="store_true",
                            help="Causes all files to be merged even if the "
                            "saved md5sum matches from a previous merge.")
        parser.add_argument("--extra-merge", action="append", nargs=2,
                            metavar="FILE", default=[],
                            help="FIXME")

    def _findTemplateDir(self):
        template_d = None
        for p in [Path(__file__).parent / "cookiecutter",
                  Path(__file__).parent.parent / "cookiecutter",
                 ]:
            if p.exists():
                template_d = p
                break
        assert template_d
        return template_d

    def _cookiecutter(self, template_d):
        try:
            cc_dir = cookiecutter(str(template_d),
                                  config_file=self.args.config_file,
                                  no_input=self.args.no_input,
                                  overwrite_if_exists=True,
                                  output_dir=self.args.outdir)
            return cc_dir
        except click.exceptions.Abort as ex:
            raise KeyboardInterrupt()  # pragma: nocover
        except CookiecutterException as ex:
            raise nicfit.CommandError("CookieCutter error: {}"
                                      .format(str(ex) if str(ex)
                                                      else ex.__class__))

    def _run(self):
        if not cookiecutter:
            raise nicfit.CommandError("CookierCutter not installed")

        cwd = Path(os.getcwd())
        clone_d = None
        if (cwd / ".git").is_dir() and not self.args.no_clone:
            pout("Cloning local repo for CookieCutter merging "
                 "(use --no-clone to disable)")
            clone_d = self._gitCloneRepo(cwd)

        # Set up user config
        if self.args.no_config:
            self.args.config_file = None
        elif not self.args.config_file:
            local_config = Path(cwd) / self.CC_USER_CONFIG
            old_local_config = Path(cwd) / self.OLD_CC_USER_CONFIG
            if local_config.is_file():
                self.args.config_file = str(local_config)
            elif old_local_config.is_file():
                self.args.config_file = str(old_local_config)
        if self.args.config_file:
            pout("Using user config ./{}, use --no-config to ignore."
                 .format(self.CC_USER_CONFIG))

        cc_dir = self._cookiecutter(self._findTemplateDir())
        if clone_d:
            copytree(str(cc_dir), str(clone_d))
            shutil.rmtree(str(cc_dir))
            os.rename(str(clone_d), str(cc_dir))

            if self.args.merge:
                self._merge(cc_dir)
                # FIXME: Handle commit-hook

    def _gitCloneRepo(self, repo_path):
        try:
            p = subprocess.run("git rev-parse --abbrev-ref HEAD", shell=True,
                               stdout=subprocess.PIPE, check=True)
            branch = str(p.stdout, "utf-8").strip()
            clone_d = Path(self.args.outdir) / str(uuid4())
            p = subprocess.run(
                "git clone --depth=1 --branch {branch} file://`pwd` {clone_d}"
                .format(**locals()),
                shell=True, stdout=subprocess.PIPE, check=True)
            return clone_d
        except subprocess.CalledProcessError as err:
            raise nicfit.CommandError(str(err))

    def _merge(self, cc_dir):
        md5_hashes = {}
        if HASH_FILE.exists():
            for line in [l.strip() for l in HASH_FILE.read_text().split("\n")]:
                if line:
                    values = line.rsplit(":", maxsplit=1)
                    if len(values) == 2 and values[0] and values[1]:
                        md5_hashes[values[0]] = values[1]

        try:
            p = subprocess.run("git -C {cc_dir} status --porcelain -uall"
                               .format(**locals()),
                               shell=True, stdout=subprocess.PIPE,
                               check=True)
            merge_files = []
            status = str(p.stdout, "utf-8").strip()
            for line in [s.strip() for s in status.split("\n")]:
                if line:
                    merge_files.append(tuple(line.split()))
        except subprocess.CalledProcessError as err:
            raise nicfit.CommandError(str(err))

        for st, file in merge_files + self.args.extra_merge:
            dst = Path(file)
            src = cc_dir / dst

            hasher = md5()
            try:
                hasher.update(src.read_bytes())
            except FileNotFoundError as notfound:
                perr(notfound)
                continue
            md5sum = hasher.hexdigest()
            merge_file = (self.args.ignore_md5s or
                          file not in md5_hashes or
                          md5sum != md5_hashes[file])
            pout("Comparing {} hash({}): {}"
                 .format(file, md5sum, Fg.blue("new")
                                        if merge_file else Fg.green("merged")))
            md5_hashes[file] = md5sum

            if not dst.exists():
                if not dst.parent.exists():
                    dst.parent.mkdir(0o755, parents=True)
                dst.touch()

            if merge_file:
                diffs = subprocess.run("diff {src} {dst} >/dev/null"
                                       .format(**locals()), shell=True)\
                                  .returncode != 0
                pout("Differences: {}".format(diffs))
                if diffs:
                    # FIXME: Allow setting of merge-tool
                    subprocess.run("meld {src} {dst}".format(**locals()),
                                   shell=True, check=True)

        with HASH_FILE.open("w") as hash_file:
            for f in sorted(md5_hashes.keys()):
                hash_file.write("{}:{}\n".format(f, md5_hashes[f]))


class Nicfit(nicfit.Application):
    def __init__(self):
        super().__init__(version=version)
        subs = self.arg_parser.add_subparsers(title="Commands",
                                              add_help_subcmd=True,
                                              dest="command")
        nicfit.Command.initAll(subs)

    def _main(self, args):
        ansi.init()
        if not args.command:
            pout(Fg.red("\m/ {} \m/".format(Style.inverse("Slayer"))))
            return 0

        try:
            return args.command_func(args)
        except nicfit.CommandError as err:
            perr(err)
            return err.exit_status


app = Nicfit()
if __name__ == "__main__":
    app.run()  # pragma: nocover

import os
import shutil
import subprocess
import collections
from uuid import uuid4
from hashlib import md5
from pathlib import Path
from tempfile import NamedTemporaryFile

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

MERGE_TOOLS = collections.OrderedDict()
MERGE_TOOLS["meld"] = None
MERGE_TOOLS["gvimdiff"] = "-geometry 169x60 -f"
MERGE_TOOLS["vimdiff"] = None


@nicfit.Command.register
class Requirements(nicfit.Command):
    """
    TODO
        - infile arg

    """
    NAME = "requirements"
    ALIASES = ["reqs"]

    def _splitPkg(self, line):
        pkg, ver = line, None
        for c in ("=", ">", "<"):
            i = line.find(c)
            if i != -1:
                pkg = line[0:i]
                ver = line[i:]
                break
        return pkg, ver

    def _readReq(self, file):
        reqs = {}
        file.seek(0)
        for line in [l.strip() for l in file.readlines()
                                  if l.strip() and not l.startswith("#")]:
            pkg, version = self._splitPkg(line)
            reqs[pkg] = version
        return reqs

    def _makeReqsFile(self, filepath, reqs):
        file_exists = filepath.exists()
        with filepath.open("r+" if file_exists else "w") as fp:
            new = {}
            curr = self._readReq(fp) if file_exists else {}

            for r in [r.strip() for r in reqs if r and r.strip()]:
                pkg, ver = self._splitPkg(r)
                if ver is None and pkg in curr:
                    ver = curr[pkg]
                new[pkg] = ver

            fp.seek(0)
            fp.truncate(0)
            for pkg in sorted(new.keys()):
                ver = new[pkg] or ""
                fp.write("{pkg}{ver}\n".format(**locals()))
            pout("Wrote {}".format(filepath))

    def _run(self):
        import yaml

        reqs_file = Path("./requirements/requirements.yml")
        if not reqs_file.exists():
            pout("Nothing to do...")
            return
        reqs_dir = reqs_file.parent

        reqs_yaml = yaml.load(reqs_file.open())

        # Make split .txt files
        for name in reqs_yaml.keys():
            if reqs_yaml[name]:
                self._makeReqsFile(reqs_dir / (name + ".txt"), reqs_yaml[name])

        # Make top-level requirements.txt files
        pkg_reqs = []
        for name, pkgs in reqs_yaml.items():
            if name == "main" or name.startswith("extra_"):
                pkg_reqs += pkgs or []
        self._makeReqsFile(Path("requirements.txt"), pkg_reqs)


@nicfit.Command.register
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
                            help="Merge two files there are outside the context"
                            " of the git repo (e.g. untracked files, "
                            ".git/hooks, etc.). This option may be specified "
                            "multiple times.")
        parser.add_argument("--merge-cmd", metavar="CMD",
                            help="Merge command. Called with with 2 args: "
                                 "<src> <dest>")

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
        except click.exceptions.Abort:
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

    def _gitCloneRepo(self, repo_path):
        try:
            p = subprocess.run("git rev-parse --abbrev-ref HEAD", shell=True,
                               stdout=subprocess.PIPE, check=True)
            branch = str(p.stdout, "utf-8").strip()
            clone_d = Path(self.args.outdir) / str(uuid4())
            p = subprocess.run(
                "git clone --depth=1 --branch {branch} file://`pwd` '{clone_d}'"
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
            p = subprocess.run("git -C \"{cc_dir}\" status --porcelain -uall"
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

            if merge_file:
                tmp_dst = None
                if not dst.exists():
                    tmp_dst = NamedTemporaryFile("w", suffix=dst.suffix,
                                                 delete=False)
                    # Write the file to exist on disk for diff and merge
                    tmp_dst.close()
                    tmp_dst = Path(tmp_dst.name)

                dst_file = str(dst if tmp_dst is None else tmp_dst)
                diffs = subprocess.run("diff '{src}' '{dst_file}' >/dev/null"
                                       .format(**locals()), shell=True)\
                                  .returncode != 0
                pout("Differences: {}".format(diffs))
                if diffs:
                    merge_cmd = self.args.merge_cmd
                    if merge_cmd is None:
                        for cmd, opts in MERGE_TOOLS.items():
                            if shutil.which(cmd):
                                merge_cmd = " ".join([cmd, opts or ""])
                                break
                    if merge_cmd is not None:
                        subprocess.run("{merge_cmd} '{src}' '{dst_file}'"
                                       .format(**locals()),
                                       shell=True, check=True)
                    else:
                        perr("Merge disabled, no merge command found. Install "
                             "a merge tool such as: {tools}.\nOr use "
                             "--merge-cmd to specify your own."
                             .format(tools=", ".join(MERGE_TOOLS.keys())))

                if tmp_dst and tmp_dst.stat().st_size == 0:
                    tmp_dst.unlink()
                elif tmp_dst:
                    # Move tmp file into place and create parent dirs
                    if not dst.parent.exists():
                        dst.parent.mkdir(0o755, parents=True)
                    shutil.move(str(tmp_dst), str(dst))

        with HASH_FILE.open("w") as hash_file:
            for f in sorted(md5_hashes.keys()):
                hash_file.write("{}:{}\n".format(f, md5_hashes[f]))


class Nicfit(nicfit.Application):
    def __init__(self):
        super().__init__(version=version, gettext_domain="nicfit.py",
                         pdb_opt=True)
        subparsers = self.arg_parser.add_subparsers(dest="command",
                                                    required=False)
        nicfit.Command.loadCommandMap(subparsers=subparsers)

    def _main(self, args):
        ansi.init()
        if "command_func" not in args or not args.command_func:
            pout(Fg.red(r"\m/ {} \m/"
                       .format(Style.inverse(_("Welcome")))))
            return 0

        try:
            return args.command_func(args)
        except nicfit.CommandError as err:
            perr(err)
            return err.exit_status


app = Nicfit()
if __name__ == "__main__":
    app.run()  # pragma: nocover

import os
import sys
import gettext
import contextlib
from pathlib import Path
from .logger import getLogger
try:
    import ipdb as _debugger
except ImportError:                                            # pragma: nocover
    import pdb as _debugger

log = getLogger(__name__)


@contextlib.contextmanager
def cd(path):
    """Context manager that changes to directory `path` and return to CWD
    when exited.
    """
    old_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old_path)


def copytree(src, dst, symlinks=True):
    """
    Modified from shutil.copytree docs code sample, merges files rather than
    requiring dst to not exist.
    """
    from shutil import copy2, Error, copystat

    names = os.listdir(src)

    if not Path(dst).exists():
        os.makedirs(dst)

    errors = []
    for name in names:
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks)
            else:
                copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except OSError as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except Error as err:
            errors.extend(err.args[0])
    try:
        copystat(src, dst)
    except OSError as why:
        # can't copy file access times on Windows
        if why.winerror is None:
            errors.extend((src, dst, str(why)))
    if errors:
        raise Error(errors)


def initGetText(domain, install=False, fallback=True):
    locale_paths = [
        Path(__file__).parent / ".." / "locale",
        Path(sys.prefix) / "share" / "locale",
    ]

    locale_dir, translation = None, None
    for locale_dir in [d for d in locale_paths if d.exists()]:
        if gettext.find(domain, str(locale_dir)):
            log.debug("Loading message catalogs from {}".format(locale_dir))
            translation = gettext.translation(domain, str(locale_dir))
            break

    if translation is None:
        # This with either throw FileNotFoundError (fallback=False) or set a
        # gettext.NullTranslations
        translation = gettext.translation(domain, str(locale_dir),
                                          fallback=fallback)
    assert translation

    if install:
        gettext.install(domain, str(locale_dir), names=["ngettext"])

    return translation


def debugger():
    """If called in the context of an exception, calls post_mortem; otherwise
    set_trace.
    ``ipdb`` is preferred over ``pdb`` if installed.
    """
    e, m, tb = sys.exc_info()
    if tb is not None:
        _debugger.post_mortem(tb)
    else:
        _debugger.set_trace()

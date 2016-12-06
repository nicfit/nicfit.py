import pytest
import logging
import logging.config
from uuid import uuid4
from io import StringIO
from nicfit._logging import *
from nicfit import _logging
from nicfit import ArgumentParser
from unittest.mock import patch, Mock


def test_log():
    # No handlers by default
    mylog = getLogger("test")
    assert isinstance(mylog, _logging.Logger)
    assert mylog.name == "test"
    assert len(mylog.handlers) == 0


    pkglog = getLogger("nicfit")
    assert isinstance(mylog, _logging.Logger)
    assert pkglog.name == "nicfit"

    for logger in [mylog, pkglog]:
        #assert(logger.getEffectiveLevel() == logging.NOTSET)
        assert(logger.propagate)
        assert(isinstance(logger, _logging.Logger))
        with patch.object(logger, "log") as mock_log:
            logger.verbose("Honey's Dead")
            mock_log.assert_called_with(logging.VERBOSE, "Honey's Dead")


def test_logLevelArguments():
    p = ArgumentParser(add_log_args=True)

    # Invalids
    for args, Exc in [(["-l"], SystemExit), (["--log-level"], SystemExit),
                      (["-l", "Vision-InTheBlinkOfAnEye"], ValueError),
                      (["-l", "debug:TheOnlyOne"], ValueError),
                     ]:
        with pytest.raises(Exc):
            _ = p.parse_args(args)

    # Level sets on root logger.
    for args, level in [(["-l", "debug"], logging.DEBUG),
                        (["-lerror"], logging.ERROR),
                        (["--log-level", "warning"], logging.WARN),
                        (["--log-level=critical"], logging.CRITICAL),
                        (["--log-level=verbose"], logging.VERBOSE),
                       ]:
        a = p.parse_args(args)
        logger = logging.getLogger()
        assert logger.getEffectiveLevel() == level

    # Level sets on other logger.
    for args, level, log in [
        (["-l", "Venom:debug"], logging.DEBUG, "Venom"),
        (["-lWatain:eRroR"], logging.ERROR, "Watain"),
        (["--log-level", "l1:WARNING"], logging.WARN, "l1"),
        (["--log-level=nicfit:critical"], logging.CRITICAL, "nicfit"),
        (["--log-level=eyeD3:verbose"], logging.VERBOSE, "eyeD3"),
    ]:
        logger = logging.getLogger(log)
        with patch.object(logger, "setLevel") as mock_log:
            a = p.parse_args(args)
        mock_log.assert_called_with(level)


def test_logFileArguments(tmpdir):
    p = ArgumentParser(add_log_args=True)

    # Invalids
    for args, Exc in [(["-L"], SystemExit), (["--log-file"], SystemExit),
                     ]:
        with pytest.raises(Exc):
            _ = p.parse_args(args)

    for args in [["-L", "<logfile>"],
                 ["-L<logfile>"],
                 ["--log-file", "<logfile>"],
                 ["--log-file=<logfile>"],
                 ["--log-file=mishmash:<logfile>"],
                 ["--log-file", "hallow:<logfile>"],
                 ["-Lsomelog:<logfile>"],
                 ["-L", "LiveLikeAnAngel:<logfile>"],
                ]:
        f = tmpdir / str(uuid4())
        assert not f.exists()
        args = [a.replace("<logfile>", str(f)) for a in args]
        a = p.parse_args(args)
        assert f.exists()

    for args in [["-L", "Bliss:stderr"],
                 ["--log-file", "Outkast:stdout"],
                 ["--log-file=Gargabe:null"],
                ]:
        a = p.parse_args(args)
        # FIXME: actually test

def test_FileConfig():
    cfg = LOGGING_CONFIG("INl3agueWitS4t4n")
    cfg_file = StringIO(cfg)
    logging.config.fileConfig(cfg_file)

def test_optSplit():
    assert(_logging._optSplit("foo") == (None, "foo"))
    assert(_logging._optSplit("foo:bazz") == ("foo", "bazz"))
    assert(_logging._optSplit("foo:bar:bazz") == ("foo", "bar:bazz"))
    assert(_logging._optSplit(":bazz") == (None, "bazz"))

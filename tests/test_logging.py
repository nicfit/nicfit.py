import sys
import pytest
import logging
import logging.config
from uuid import uuid4
from io import StringIO
from unittest.mock import patch, Mock, call
import deprecation
from nicfit.logger import getLogger, FileConfig, DictConfig
from nicfit import logger
from nicfit import ArgumentParser


def test_log():
    # No handlers by default
    mylog = getLogger("test")
    assert isinstance(mylog, logger.Logger)
    assert mylog.name == "test"
    assert len(mylog.handlers) == 0

    pkglog = getLogger("nicfit")
    assert isinstance(mylog, logger.Logger)
    assert pkglog.name == "nicfit"

    for log in [mylog, pkglog]:
        assert(log.propagate)
        assert(isinstance(log, logger.Logger))
        with patch.object(log, "log") as mock_log:
            log.verbose("Honey's Dead")
            mock_log.assert_called_with(logging.VERBOSE, "Honey's Dead")


def test_logLevelArguments():
    p = ArgumentParser(add_log_args=True)

    # Invalids
    for args, Exc in [(["-l"], SystemExit), (["--log-level"], SystemExit),
                      (["-l", "Vision-InTheBlinkOfAnEye"], ValueError),
                      (["-l", "debug:TheOnlyOne"], ValueError),
                     ]:
        with pytest.raises(Exc):
            p.parse_args(args)

    # Level sets on root logger.
    for args, level in [(["-l", "debug"], logging.DEBUG),
                        (["-lerror"], logging.ERROR),
                        (["--log-level", "warning"], logging.WARN),
                        (["--log-level=critical"], logging.CRITICAL),
                        (["--log-level=verbose"], logging.VERBOSE),
                       ]:
        p.parse_args(args)
        logger = getLogger()
        assert logger.getEffectiveLevel() == level

    # Level sets on other logger.
    for args, level, log in [
        (["-l", "Venom:debug"], logging.DEBUG, "Venom"),
        (["-lWatain:eRroR"], logging.ERROR, "Watain"),
        (["--log-level", "l1:WARNING"], logging.WARN, "l1"),
        (["--log-level=nicfit:critical"], logging.CRITICAL, "nicfit"),
        (["--log-level=eyeD3:verbose"], logging.VERBOSE, "eyeD3"),
    ]:
        logger = getLogger(log)
        with patch.object(logger, "setLevel") as mock_log:
            p.parse_args(args)
        mock_log.assert_called_with(level)


def test_logFileArguments(tmpdir):
    p = ArgumentParser(add_log_args=True)

    # Invalids
    for args, Exc in [(["-L"], SystemExit), (["--log-file"], SystemExit),
                     ]:
        with pytest.raises(Exc):
            p.parse_args(args)

    # Load up a logger with a log of handlers to
    parentlog = getLogger("parentlog")
    parentlog.addHandler(Mock())
    parentlog.addHandler(Mock())
    _ = getLogger("parentlog.child1")

    for args in [["-L", "<logfile>"],
                 ["-L<logfile>"],
                 ["--log-file", "<logfile>"],
                 ["--log-file=<logfile>"],
                 ["--log-file=mishmash:<logfile>"],
                 ["--log-file", "hallow:<logfile>"],
                 ["-Lsomelog:<logfile>"],
                 ["-Lparentlog.child1.child2:<logfile>"],
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
        _ = p.parse_args(args)
        # FIXME: actually test


def test_FileConfig():
    cfg = "\n".join([FileConfig.DEFAULT_LOGGING_CONFIG(),
                     FileConfig.PKG_LOGGING_CONFIG("INl3agueWitS4t4n")])
    cfg_file = StringIO(cfg)
    logging.config.fileConfig(cfg_file)


def test_DictConfig():
    cfg = DictConfig.DEFAULT_LOGGING_CONFIG()
    #cfg.update(DictConfig.PKG_LOGGING_CONFIG("INl3agueWitS4t4n"))
    logging.config.dictConfig(cfg)


def test_optSplit():
    assert(logger._optSplit("foo") == (None, "foo"))
    assert(logger._optSplit("foo:bazz") == ("foo", "bazz"))
    assert(logger._optSplit("foo:bar:bazz") == ("foo", "bar:bazz"))
    assert(logger._optSplit(":bazz") == (None, "bazz"))


def test_applyLogOpts():
    mock_setLevel = Mock()
    mock_addHandler = Mock()

    mock_def_logger = Mock()
    mock_def_logger.handlers = ["DummyHandler", "AnotherDummyHandler"]
    mock_eyeD3_logger = Mock()
    mock_eyeD3_logger.handlers = []
    for l in [mock_def_logger, mock_eyeD3_logger]:
        l.setLevel = mock_setLevel
        l.addHandler = mock_addHandler

    p = ArgumentParser(add_log_args=True)
    args = p.parse_args(["-ldebug", "-L", "log.log", "--log-level", "warning",
                         "--log-level=eyeD3:error"])
    for arg_list in [args.log_levels, args.log_files]:
        for i in range(len(arg_list)):
            if arg_list[i][0] is getLogger():
                mock_logger = mock_def_logger
            elif arg_list[i][0] is getLogger("eyeD3"):
                mock_logger = mock_eyeD3_logger
            else:
                pytest.fail("Unhandled logger")
            arg_list[i] = (mock_logger, arg_list[i][1])

    args.applyLoggingOpts(args.log_levels, args.log_files)
    assert mock_setLevel.call_count == 3
    mock_setLevel.assert_has_calls([call(logging.DEBUG), call(logging.WARN),
                                    call(logging.ERROR)])
    assert mock_addHandler.call_count == 1
    assert getLogger().getEffectiveLevel() == logging.WARN
    assert getLogger("eyeD3").getEffectiveLevel() == logging.ERROR

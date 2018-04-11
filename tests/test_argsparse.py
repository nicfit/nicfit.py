import sys
import pytest
from argparse import ArgumentTypeError
from unittest.mock import MagicMock as Mock
from nicfit import ArgumentParser
from nicfit import ConfigOpts

LOG_LEVEL_ARGS = [("-l", "debug"), ("-lerror",),
                  ("--log-level", "debug"), ("--log-level=critical",),
                  ("-l", "log1:debug"), ("-llog2:error",),
                  ("--log-level", "log3:debug"), ("--log-level=log4:critical",),
                 ]

LOG_FILE_ARGS = [("-L", "all.log"), ("-Lall.log",),
                  ("--log-file", "all.log"), ("--log-file=all.log",),
                  ("-L", "log1:log1.log"), ("-Llog2:log2.log",),
                  ("--log-file", "log3:log3.log"), ("--log-file=log4:log4.log",),
                 ]

CONFIG_FILE_ARGS = [("-c", "config.ini"), ("-cconfig.ini",),
                    ("--config", "config.ini"), ("--config=config.ini",),
                   ]


def test_ArgumentParser_default():
    p = ArgumentParser()

    # All logging opts are off by default
    for args in LOG_LEVEL_ARGS + LOG_FILE_ARGS:
        with pytest.raises(SystemExit):
            args = p.parse_args(args)

    # All config opts are off by default
    for args in CONFIG_FILE_ARGS + [("--config-override", "SECTION:OPT=VAL")]:
        with pytest.raises(SystemExit):
            args = p.parse_args(args)


def test_default_config_arg(capfd):
    config = "[ini]\ntest = SAMPLE CONFIG"
    p = ArgumentParser(config_opts=ConfigOpts(default_config=config,
                                              default_config_opt="--DEFAULT"))
    p.exit = Mock()

    _ = p.parse_args(["--DEFAULT"])
    p.exit.assert_called_once_with(0)
    out, _ = capfd.readouterr()
    assert out == config + "\n"


def test_default_config_opt_no_arg():
    with pytest.raises(ValueError):
        ArgumentParser(config_opts=ConfigOpts(default_config=None,
                                              default_config_opt="--DEFAULT"))


def test_ArgumentParser_add_subparsers():
    with pytest.raises(SystemExit):
        ArgumentParser().parse_args(["help"])

    p = ArgumentParser()
    p.add_subparsers(dest="cmd", add_help_subcmd=True)
    args = p.parse_args(["help"])
    assert args.command is None
    assert args.command_func is not None

    p = ArgumentParser()
    p.add_subparsers(dest="cmd", add_help_subcmd=True)
    args = p.parse_args(["help", "cmd"])
    assert args.command is "cmd"
    assert args.command_func is not None
    # Help func may called parse_args again, or print_help. mock em.
    p.parse_args = Mock()
    p.print_help = Mock()
    with pytest.raises(SystemExit):
        args.command_func(args)
    p.parse_args.assert_called_with(["cmd", "--help"])
    p.print_help.assert_not_called()

    p.parse_args.reset_mock()
    p.print_help.reset_mock()
    with pytest.raises(SystemExit):
        args.command = None
        args.command_func(args)
    if sys.version_info[:2] >= (3, 6):
        p.print_help.assert_called_once()
    else:
        assert p.print_help.call_count == 1
    p.parse_args.assert_not_called()

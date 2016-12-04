import pytest
from nicfit import ArgumentParser

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

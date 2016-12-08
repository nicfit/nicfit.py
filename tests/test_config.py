import os.path
import tempfile
import argparse
import configparser
from pathlib import Path
from os.path import expandvars, expanduser, join, sep

import pytest

from nicfit import Config
from nicfit import ConfigOpts
from nicfit import ArgumentParser
from nicfit._config import ConfigFileType, _config_override


def test_ConfigOpts():
    opts = ConfigOpts()
    assert not opts.required
    assert opts.default_file is None
    assert opts.default_config is None
    assert opts.ConfigClass is Config

    class MyConfig(Config):
        pass
    opts = ConfigOpts(required=True, ConfigClass=MyConfig,
                      default_file="config.ini", default_config="foobar")
    assert opts.required
    assert opts.default_file is "config.ini"
    assert opts.default_config is "foobar"
    assert opts.ConfigClass is MyConfig

    config = Config("/tmp/config.ini")
    assert(str(config.filename) == "/tmp/config.ini")
    config = Config("$HOME/config.ini")
    assert(str(config.filename) == join(expandvars("$HOME"), "config.ini"))
    config = Config("~/config.ini")
    assert(str(config.filename) == join(expanduser("~"), "config.ini"))
    config = Config("~/${HOME}/config.ini")

    filename = filename2 = None
    fn, filename = tempfile.mkstemp()
    os.close(fn)
    try:
        config = Config(filename)

        config.add_section("1")
        config.set("1", "one", "uno")
        config.add_section("2")
        config.set("2", "two", "dos")
        config.add_section("3")
        config.set("3", "three", "tres")

        config.write()

        config2 = Config(filename)
        config2.read()
        assert(config2.get("1", "one") == "uno")
        assert(config2.get("2", "two") == "dos")
        assert(config2.get("3", "three") == "tres")

        fn, filename2 = tempfile.mkstemp()
        os.close(fn)

        with open(filename2, 'w') as fp:
            config2.write(fileobject=fp)
        config3 = Config(filename2)
        config3.read()
        assert(config3.get("1", "one") == "uno")
        assert(config3.get("2", "two") == "dos")
        assert(config3.get("3", "three") == "tres")

    finally:
        if filename is not None:
            os.unlink(filename)
        if filename2 is not None:
            os.unlink(filename2)


def test_ConfigConstructor():
    c = Config("file.ini")
    assert isinstance(c, configparser.ConfigParser)
    assert isinstance(c.filename, Path)
    assert str(c.filename) == "file.ini"

    os.environ["var1"] = "foo"
    os.environ["var2"] = "bazz"
    c = Config("~/dir/${var1}/${var2}/config.ini")
    assert str(c.filename) == os.path.expanduser("~/dir/foo/bazz/config.ini")


def test_ConfigRead(tmpdir):
    filename = os.path.join(str(tmpdir), "config.ini")

    # File not found
    c = Config(filename)
    with pytest.raises(FileNotFoundError):
        c.read()

    # File not found, but use touch option
    assert not Path(filename).exists()
    c.read(touch=True)
    assert Path(filename).exists()
    assert c.sections() == []

    with open(filename, "w") as fp:
        fp.write(SAMPLE_CONFIG1)
    c = Config(filename)
    c.read()
    assert set(c.sections()) == {"MAIN", "CONFIG1"}


def test_ConfigReadMulti(tmpdir):
    all_files = []
    for i, cfg in enumerate([SAMPLE_CONFIG1, SAMPLE_CONFIG2,
                             SAMPLE_CONFIG3], 1):
        filename = os.path.join(str(tmpdir), "config{:d}.ini".format(i))
        with open(filename, "w") as fp:
            fp.write(cfg)
        all_files.append(filename)

    filename = os.path.join(str(tmpdir), "config4.ini")
    c = Config(filename)
    c.read(filenames=all_files, touch=True)
    assert set(c.sections()) == {"MAIN", "CONFIG1", "CONFIG2", "CONFIG3"}
    assert c.get("MAIN", "mainkey") == "config3"

    all_files.reverse()

    c = Config(filename)
    c.read(filenames=all_files, touch=True)
    assert set(c.sections()) == {"MAIN", "CONFIG1", "CONFIG2", "CONFIG3"}
    assert c.get("MAIN", "mainkey") == "config1"


def test_ConfigWrite(tmpdir):
    filename = os.path.join(str(tmpdir), "config.ini")
    c = Config(filename)
    c.read_string(SAMPLE_CONFIG1)
    c.write()

    c2 = Config(filename)
    c2.read()
    assert [i for i in c.items()] == [i for i in c2.items()]

    fpfile = os.path.join(str(tmpdir), "configfp.ini")
    with open(fpfile, "w") as fp:
        c2.write(fp)
    c3 = Config(fpfile)
    c3.read()
    assert [i for i in c3.items()] == [i for i in c2.items()]


def test_ConfigFileType(tmpdir):
    cfgtype = ConfigFileType()
    assert isinstance(cfgtype, argparse.FileType)
    assert cfgtype._encoding == "utf-8"
    assert cfgtype._opts.default_config == None

    # File does not exist
    f = os.path.join(str(tmpdir), "dne")
    with pytest.raises(argparse.ArgumentTypeError):
        cfgtype(f)

    # File does not exist, but provide a default config
    f = os.path.join(str(tmpdir), "default")
    cfgtype = ConfigFileType(ConfigOpts(default_config=SAMPLE_CONFIG3))
    assert cfgtype._opts.default_config == SAMPLE_CONFIG3
    config = cfgtype(f)
    assert isinstance(config, Config)
    assert str(config.filename) == f
    config.write()
    copy = Config(f)
    copy.read()
    assert [i for i in copy.items()] == [i for i in config.items()]


    # File exists
    f = os.path.join(str(tmpdir), "exists")
    with open(f, "w") as fp:
        fp.write(SAMPLE_CONFIG3)
    cfgtype = ConfigFileType()
    existing = cfgtype(f)
    assert [i for i in existing.items()] == [i for i in config.items()]


def test_ConfigArgumentParser(tmpdir):
    # A config is optional, so a -c/--config arg was added
    p = ArgumentParser(config_opts=ConfigOpts())
    args = p.parse_args([])

    # No arg value
    with pytest.raises(SystemExit):
        args = p.parse_args(["-c"])
    with pytest.raises(SystemExit):
        args = p.parse_args(["--config"])

    # Arg value, but config does not exist
    with pytest.raises(SystemExit):
        args = p.parse_args(["-c", "dne"])
    with pytest.raises(SystemExit):
        args = p.parse_args(["--config", "dne"])

    # Arg value, config does not exist, but a default was given.
    p = ArgumentParser(config_opts=ConfigOpts(default_config=SAMPLE_CONFIG1))
    f = os.path.join(str(tmpdir), "default.ini")
    args = p.parse_args(["-c", f])
    assert args.config is not None
    sample1 = configparser.ConfigParser()
    sample1.read_string(SAMPLE_CONFIG1)
    assert [i for i in args.config.items()] == [i for i in sample1.items()]

    # A config is required, so positional config argument is added
    p = ArgumentParser(config_opts=ConfigOpts(required=True))
    with pytest.raises(SystemExit):
        args = p.parse_args([])

    f = os.path.join(str(tmpdir), "default.ini")
    # Arg value, but config does not exist
    with pytest.raises(SystemExit):
        args = p.parse_args([f])

    sample3 = Config(f)
    sample3.read_string(SAMPLE_CONFIG3)
    sample3.write()
    args = p.parse_args([f])
    assert [i for i in args.config.items()] == [i for i in sample3.items()]


def test_ConfigOverrides(tmpdir):
    sample2 = Config("sample2")
    sample2.read_string(SAMPLE_CONFIG2)

    f = os.path.join(str(tmpdir), "default.ini")
    p = ArgumentParser(config_opts=ConfigOpts(required=True,
                                              override_arg=True,
                                              default_file=f,
                                              default_config=SAMPLE_CONFIG2))
    args = p.parse_args([])
    assert args.config is not None
    assert [i for i in args.config.items()] == [i for i in sample2.items()]
    assert args.config.get("MAIN", "mainkey") == "config2"

    args = p.parse_args(["--config-override=MAIN:mainkey=2gifnoc",
                         "--config-override=CONFIG2:key=value2",
                         "--config-override=NEWSECT:special=value",
                         ])
    assert args.config.get("MAIN", "mainkey") == "2gifnoc"
    assert args.config.get("CONFIG2", "key") == "value2"
    assert args.config.get("NEWSECT", "special") == "value"


def test_ConfigOverridesWrongParserType(tmpdir):
    from nicfit._config import addCommandLineArgs
    p = argparse.ArgumentParser()
    with pytest.raises(ValueError):
        addCommandLineArgs(p, ConfigOpts(override_arg=True))


SAMPLE_CONFIG1 = """
[MAIN]
mainkey = config1

[CONFIG1]
key = value
"""

SAMPLE_CONFIG2 = """
[MAIN]
mainkey = config2
[CONFIG2]
KEY = value
"""

SAMPLE_CONFIG3 = """
[MAIN]
mainkey = config3

[CONFIG3]
key = value
"""

def test_configoverride_argtype():
    assert _config_override("sect:key=val") == ("sect", ("key", "val"))
    for val in ("sect", "sect:key", "sect:=val", ":key=", ":="):
        with pytest.raises(ValueError):
            _config_override(val)

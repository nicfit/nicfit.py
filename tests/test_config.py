import os
import tempfile
import argparse
import configparser
import logging.config
from pathlib import Path
from unittest.mock import patch

import pytest

from nicfit import Config
from nicfit import ConfigOpts
from nicfit import ArgumentParser
from nicfit.config import ConfigFileType, _config_override


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

    tmp_config = Path("/tmp/nicfit-test.ini")
    tmp_config.exists() and tmp_config.unlink()
    with pytest.raises(FileNotFoundError):
        _ = Config("/tmp/config.ini")

    filename2 = None
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


def test_ConfigConstructor(tmpdir):
    file = str(tmpdir.join("file.ini"))
    c = Config(file, touch=True)
    assert isinstance(c, configparser.ConfigParser)
    assert isinstance(c.filename, Path)
    assert str(c.filename) == file

    file = str(tmpdir.join("subdir", "dir/${var1}/${var2}/config.ini"))
    os.environ["var1"] = "foo"
    os.environ["var2"] = "bazz"
    c = Config(file, touch=True)
    assert c.filename.exists()
    assert str(c.filename) == "{}/subdir/dir/foo/bazz/config.ini".format(tmpdir)


def test_ConfigRead(tmpdir):
    filename = os.path.join(str(tmpdir), "config.ini")

    # File not found
    with pytest.raises(FileNotFoundError):
        c = Config(filename)

    # File not found, but use touch option
    c = Config(filename, touch=True)
    c.read()
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
    c = Config(filename, touch=True)
    c.read(filenames=all_files)
    assert set(c.sections()) == {"MAIN", "CONFIG1", "CONFIG2", "CONFIG3"}
    assert c.get("MAIN", "mainkey") == "config3"

    all_files.reverse()

    c = Config(filename, touch=True)
    c.read(filenames=all_files)
    assert set(c.sections()) == {"MAIN", "CONFIG1", "CONFIG2", "CONFIG3"}
    assert c.get("MAIN", "mainkey") == "config1"


def test_ConfigWrite(tmpdir):
    filename = os.path.join(str(tmpdir), "config.ini")
    c = Config(filename, touch=True)
    c.read_string(SAMPLE_CONFIG1)
    c.write()

    c2 = Config(filename, touch=True)
    c2.read()
    assert [i for i in c.items()] == [i for i in c2.items()]

    fpfile = os.path.join(str(tmpdir), "configfp.ini")
    with open(fpfile, "w") as fp:
        c2.write(fp)
    c3 = Config(fpfile, touch=True)
    c3.read()
    assert [i for i in c3.items()] == [i for i in c2.items()]


def test_ConfigFileType(tmpdir):
    cfgtype = ConfigFileType()
    assert isinstance(cfgtype, argparse.FileType)
    assert cfgtype._encoding == "utf-8"
    assert cfgtype._opts.default_config == None

    # File does not exist
    f = os.path.join(str(tmpdir), "dne")
    with pytest.raises(FileNotFoundError):
        cfgtype(f)

    # File does not exist, but provide a default config
    f = os.path.join(str(tmpdir), "default")
    with pytest.raises(FileNotFoundError):
        cfgtype = ConfigFileType(ConfigOpts(default_config=SAMPLE_CONFIG3,
                                            touch=False))
        assert cfgtype._opts.default_config == SAMPLE_CONFIG3
        config = cfgtype(f)
    # ... touch == True
    cfgtype = ConfigFileType(ConfigOpts(default_config=SAMPLE_CONFIG3,
                                        touch=True))
    assert cfgtype._opts.default_config == SAMPLE_CONFIG3
    config = cfgtype(f)
    assert isinstance(config, Config)
    assert str(config.filename) == f
    config.write()
    copy = Config(f, touch=True)
    copy.read()
    assert [i for i in copy.items()] == [i for i in config.items()]

    # File exists
    f = os.path.join(str(tmpdir), "exists")
    with open(f, "w") as fp:
        fp.write(SAMPLE_CONFIG3)
    cfgtype = ConfigFileType()
    existing = cfgtype(f)
    assert [i for i in existing.items()] == [i for i in config.items()]


def test_ConfigArgumentParserDNE():
    # A config is optional, so a -c/--config arg was added
    p = ArgumentParser(config_opts=ConfigOpts())
    args = p.parse_args([])

    # Arg value, but config does not exist
    with pytest.raises(FileNotFoundError):
        args = p.parse_args(["-c", "dne"])
    with pytest.raises(FileNotFoundError):
        args = p.parse_args(["--config", "dne"])

    # No arg value
    with pytest.raises(SystemExit):
        args = p.parse_args(["-c"])
    with pytest.raises(SystemExit):
        args = p.parse_args(["--config"])


def test_ConfigArgumentParser(tmpdir):
    # A config is optional, so a -c/--config arg was added
    p = ArgumentParser(config_opts=ConfigOpts())
    args = p.parse_args([])

    # Arg value, config does not exist, but a default was given.
    p = ArgumentParser(config_opts=ConfigOpts(default_config=SAMPLE_CONFIG1))
    f = os.path.join(str(tmpdir), "default.ini")
    Path(f).touch()
    args = p.parse_args(["-c", f])
    assert args.config is not None
    sample1 = configparser.ConfigParser()
    sample1.read_string(SAMPLE_CONFIG1)
    assert [i for i in args.config.items()] == [i for i in sample1.items()]

    # A config is required, so positional config argument is added
    p = ArgumentParser(config_opts=ConfigOpts(required=True))
    with pytest.raises(SystemExit):
        args = p.parse_args([])

    f = os.path.join(str(tmpdir), "bluntsAndAstrays.ini")
    # Arg value, but config does not exist
    with pytest.raises(FileNotFoundError):
        args = p.parse_args([f])

    sample3 = Config(f, touch=True)
    sample3.read_string(SAMPLE_CONFIG3)
    sample3.write()
    args = p.parse_args([f])
    assert [i for i in args.config.items()] == [i for i in sample3.items()]


def test_ConfigOverrides(tmpdir):
    sample2 = Config(None)
    sample2.read_string(SAMPLE_CONFIG2)

    f = os.path.join(str(tmpdir), "default.ini")
    Path(f).touch()
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
    from nicfit.config import addCommandLineArgs
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


def test_env_config(tmpdir):
    config_path = tmpdir.join("config.ini")
    new_config = tmpdir.join("new.ini")
    assert not config_path.exists()
    assert not new_config.exists()
    config_path.write(SAMPLE_CONFIG1)
    os.environ["CONFIG_VAR"] = str(config_path)

    c = Config(tmpdir / "file.ini", config_env_var="CONFIG_VAR", touch=True)
    assert c.sections() == ["MAIN", "CONFIG1"]
    assert c["MAIN"]["mainkey"] == "config1"
    assert c["CONFIG1"]["key"] == "value"


def test_Config_getlist():
    c = Config(None)
    c.add_section("section")

    c.set("section", "key", "")
    assert c.getlist("section", "key") == []

    c.set("section", "key", "1")
    assert c.getlist("section", "key") == ["1"]

    c.set("section", "key", "1,2")
    assert c.getlist("section", "key") == ["1", "2"]
    c.set("section", "key", "1,2 ")
    assert c.getlist("section", "key") == ["1", "2"]
    c.set("section", "key", " 1, 2 ")
    assert c.getlist("section", "key") == ["1", "2"]

    c.set("section", "key", ",2")
    assert c.getlist("section", "key") == ["", "2"]
    c.set("section", "key", "1,")
    assert c.getlist("section", "key") == ["1", ""]
    c.set("section", "key", ",2,")
    assert c.getlist("section", "key") == ["", "2", ""]

    c.set("section", "key", "1,2,3,4,5\n6\n7\n8,9\n10")
    assert c.getlist("section", "key") == [str(i) for i in range(1, 11)]
    c.set("section", "key", "\n6\n7\n8,9\n\n\n10")
    assert c.getlist("section", "key") == ["", "6", "7", "8", "9", "", "", "10"]


def test_Config_touch(tmpdir):
    filename = Path(str(tmpdir)) / "subdir" / "config.ini"

    with pytest.raises(FileNotFoundError):
        _ = Config(filename)
    assert filename.exists() == False

    cfg = Config(filename, touch=True)
    assert str(filename) == str(cfg.filename)
    assert filename.exists() == True


def test_Config_mode(tmpdir):
    filename1 = Path(str(tmpdir)) / "subdir" / "config.ini"
    filename2 = Path(str(tmpdir)) / "subdir" / "config2.ini"

    curr_umask = os.umask(0)
    os.umask(curr_umask)

    # Touch without mode should produce a file per umask
    cfg = Config(filename1, touch=True)
    assert str(filename1) == str(cfg.filename)
    assert filename1.exists() == True
    assert (filename1.stat().st_mode & 0o000777) == (0o666 ^ curr_umask)

    cfg = Config(filename2, touch=True, mode=0o600)
    assert str(filename2) == str(cfg.filename)
    assert filename2.exists() == True
    assert (filename2.stat().st_mode & 0o000777) == 0o600


def test_Config_setlist(tmpdir):
    c = Config(str(tmpdir / "test.ini"), touch=True)
    items = [1, 2, 3, 13, 11, 6]
    c.add_section("sect")
    c.setlist("sect", "opt", items)
    assert c.get("sect", "opt") == "1, 2, 3, 13, 11, 6"
    assert c.getlist("sect", "opt") == ["1", "2", "3", "13", "11", "6"]

    # Config __str__ test.
    assert str(c) == "[sect]\nopt = 1, 2, 3, 13, 11, 6\n\n"


def test_ConfigFileType_loggingConfig(tmpdir):
    inifile = tmpdir / "bornagainst.ini"

    # init_logging_fileConfig
    with patch.object(logging.config, "fileConfig"):
        cfg_ftype = ConfigFileType(ConfigOpts(init_logging_fileConfig=True,
                                              touch=True))
        config = cfg_ftype(str(inifile))
        logging.config.fileConfig.assert_called_once_with(config)


def test_Config_read_dict(tmpdir):
    inifile = tmpdir / "Pestilence.ini"
    cfg = Config(inifile, touch=True)
    cfg.read_dict({"Born Against" : {"from": "USA",
                                     "hardcore": "yes"
                                    },
                   "Altar": {"from": "Netherlands",
                             "hardcore": "no"
                            },
                   "Pestilence": {"from": "Netherlands",
                                  "hardcore": "no"
                                 }
                  })
    assert set(cfg.sections()) == {"Altar", "Born Against", "Pestilence"}
    assert not cfg.getboolean("Pestilence", "hardcore")
    assert not cfg.getboolean("Altar", "hardcore")
    assert cfg.getboolean("Born Against", "hardcore")
    assert cfg.get("Born Against", "from") == "USA"
    assert cfg.get("Altar", "from") == "Netherlands"
    assert cfg.get("Pestilence", "from") == "Netherlands"

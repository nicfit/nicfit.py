import pytest
from deprecation import fail_if_not_removed
from unittest.mock import MagicMock as Mock
from nicfit.command import Command, CommandError, SubCommandCommand


def _assert_called_once(mocked):
    """Needed for pypy support even though nicfit.py support is 3.6 and above"""
    import sys
    if sys.version_info[:2] >= (3, 6):
        mocked.assert_called_once()
    else:
        assert mocked.call_count == 1


@pytest.fixture
def emptycommands():
    Command._registered_commands.clear()


def test_loadCommandMap_Empty(emptycommands):
    with pytest.raises(ValueError):
        Command.loadCommandMap(Mock())


def test_register(emptycommands):
    @Command.register
    class c1(Command):
        def __init__(self, foo=None, **kwargs):
            super().__init__(**kwargs)
            self.foo = foo

    @Command.register
    class c2(Command):
        def __init__(self, foo=None, **kwargs):
            super().__init__(**kwargs)
            self.foo = foo

    assert len(Command._registered_commands) == 1
    assert len(Command._registered_commands[Command]) == 2
    map = Command.loadCommandMap(subparsers=Mock(spec=["add_parser"]),
                                 foo="Cobalt - Gin")
    assert len(map) == 2
    assert map["c1"].foo == "Cobalt - Gin"
    assert map["c2"].foo == "Cobalt - Gin"

    class MoreCommands(Command):
        pass

    @MoreCommands.register
    class c1(Command):
        def __init__(self, foo=None, **kwargs):
            super().__init__(**kwargs)
            self.foo = foo

    @MoreCommands.register
    class c2(Command):
        def __init__(self, foo=None, **kwargs):
            super().__init__(**kwargs)
            self.foo = foo

    assert len(Command._registered_commands) == 2
    assert len(Command._registered_commands[Command]) == 2
    assert len(Command._registered_commands[MoreCommands]) == 2
    map = MoreCommands.loadCommandMap(subparsers=Mock(spec=["add_parser"]),
                                      foo="24-7 Spyz - Stuntman")
    assert len(map) == 2
    assert map["c1"].foo == "24-7 Spyz - Stuntman"
    assert map["c2"].foo == "24-7 Spyz - Stuntman"


def test_dup_register(emptycommands):
    @Command.register
    class c1(Command): pass # noqa

    @Command.register
    class c2(Command): pass # noqa

    with pytest.raises(ValueError):
        @Command.register
        class c2dup(Command):
            NAME = "c2"

    assert len(Command._registered_commands[Command]) == 2


def test_run_notimplemented(emptycommands):
    @Command.register
    class TestCommand(Command):
        pass

    with pytest.raises(NotImplementedError):
        TestCommand().run(None)


def test_run(emptycommands):
    @Command.register
    class TestCommand(Command):
        NAME = "test"
        _initArgParser = Mock()
        _run = Mock()

    mock_args = Mock()
    mock_parser = Mock()
    mock_parser.set_defaults = Mock()
    mock_subparser = Mock()
    mock_subparser.add_parser = Mock(return_value=mock_parser)

    assert len(Command._registered_commands[Command]) == 1
    cmd = Command.loadCommandMap(subparsers=mock_subparser,
                                 aesop="Rock", Brian="Jonestown")["test"]

    assert cmd.subparsers is mock_subparser
    assert cmd.parser is mock_parser
    cmd._initArgParser.assert_called_once_with(mock_parser)

    assert cmd.aesop == "Rock"
    assert cmd.Brian == "Jonestown"

    cmd.run(mock_args)
    _assert_called_once(cmd._run)
    assert cmd.args is mock_args
    mock_parser.set_defaults.assert_called_once_with(command_func=cmd.run)


def test_run_exit_status(emptycommands):
    mock_subparser = Mock(spec=["add_parser"])

    @Command.register
    class CNone(Command):
        def _run(self):
            pass

    assert CNone(mock_subparser).run(None) is None

    @Command.register
    class C0(Command):
        def _run(self):
            return 0

    assert C0(mock_subparser).run(None) == 0

    @Command.register
    class C99(Command):
        def _run(self):
            return 99

    assert C99(mock_subparser).run(None) == 99

    @Command.register
    class CErr(Command):
        def _run(self):
            raise CommandError("The Faint", 6)

    with pytest.raises(CommandError) as err:
        assert CErr(mock_subparser).run(None) == 6
    assert str(err.value) == "The Faint"
    assert err.value.exit_status == 6

    @Command.register
    class CExc(Command):
        def _run(self):
            raise ValueError("Danse Macabre")

    with pytest.raises(ValueError):
        CExc(mock_subparser).run(None)


def test_subcommands(emptycommands):
    run_body_mock2 = Mock()
    run_body_mock3 = Mock()

    class sub1(Command):
        ...
    class sub2(Command):
        def _run(self):
            run_body_mock2()
    class sub3(Command):
        def _run(self):
            run_body_mock3()

    @Command.register
    class TopLevelCommand(SubCommandCommand):
        SUB_CMDS = [sub1, sub2, sub3]
        NAME = "top1"
        ALIASES = ["T", "t1"]

    @Command.register
    class TopLevelCommand2(SubCommandCommand):
        NAME = "top2"
        SUB_CMDS = [sub1, sub3]
        DEFAULT_CMD = sub3

    assert len(Command._registered_commands[Command]) == 4
    loaded = Command.loadCommandMap()
    assert len(loaded) == 4

    assert id(loaded["top1"]) == id(loaded["T"]) == id(loaded["t1"])

    command = loaded["top1"]
    command.run(command.parser.parse_args(["sub2"]))
    _assert_called_once(run_body_mock2)

    command = loaded["top2"]
    command.run(command.parser.parse_args([]))
    _assert_called_once(run_body_mock3)


## BEGIN DEPRECATED ##
from nicfit.command import register


@fail_if_not_removed
def test_initAllEmpty_DEPRECATED():
    Command._all_commands.clear()
    with pytest.raises(ValueError):
        Command.initAll(Mock())


@fail_if_not_removed
def test_register_DEPRECATED():
    Command._all_commands.clear()

    @register
    class c1(Command): pass # noqa

    @register
    class c2(Command): pass # noqa

    assert len(Command._all_commands) == 2
    Command.initAll(Mock(spec=["add_parser"]))


@fail_if_not_removed
def test_register_interCommands_DEPRECATED():
    Command._all_commands.clear()

    @register
    class c1(Command): pass # noqa

    @register
    class c2(Command): pass # noqa

    @register
    class c3(Command): pass # noqa

    assert len(Command._all_commands) == 3
    all = Command.iterCommands()
    assert len(list(all)) == 3


@fail_if_not_removed
def test_dup_register_DEPRECATED():
    Command._all_commands.clear()

    @register
    class c1(Command): pass # noqa

    @register
    class c2(Command): pass # noqa

    with pytest.raises(ValueError):
        @register
        class c2dup(Command):
            NAME = "c2"

    assert len(Command._all_commands) == 2
    Command.initAll(Mock(spec=["add_parser"]))


@fail_if_not_removed
def test_run_notimplemented_DEPRECATED():
    Command._all_commands.clear()

    @register
    class TestCommand(Command):
        pass
    Command.initAll(Mock(spec=["add_parser"]))

    with pytest.raises(NotImplementedError):
        TestCommand(Mock()).run(None)


@fail_if_not_removed
def test_run_DEPRECATED():
    Command._all_commands.clear()

    @register
    class TestCommand(Command):
        NAME = "test"
        _initArgParser = Mock()
        _run = Mock()

    mock_args = Mock()
    mock_parser = Mock()
    mock_parser.set_defaults = Mock()
    mock_subparser = Mock()
    mock_subparser.add_parser = Mock(return_value=mock_parser)

    cmd = Command.initAll(mock_subparser)[0]
    assert len(Command._all_commands) == 1

    assert cmd.subparsers is mock_subparser
    assert cmd.parser is mock_parser
    cmd._initArgParser.assert_called_once_with(mock_parser)

    cmd.run(mock_args)
    _assert_called_once(cmd._run)
    assert cmd.args is mock_args
    mock_parser.set_defaults.assert_called_once_with(command_func=cmd.run)


@fail_if_not_removed
def test_run_exit_status_DEPRECATED():
    Command._all_commands.clear()

    mock_subparser = Mock(spec=["add_parser"])

    @register
    class CNone(Command):
        def _run(self):
            pass

    assert CNone(mock_subparser).run(None) is None

    @register
    class C0(Command):
        def _run(self):
            return 0

    assert C0(mock_subparser).run(None) == 0

    @register
    class C99(Command):
        def _run(self):
            return 99

    assert C99(mock_subparser).run(None) == 99

    @register
    class CErr(Command):
        def _run(self):
            raise CommandError("The Faint", 6)

    with pytest.raises(CommandError) as err:
        assert CErr(mock_subparser).run(None) == 6
    assert str(err.value) == "The Faint"
    assert err.value.exit_status == 6

    @register
    class CExc(Command):
        def _run(self):
            raise ValueError("Danse Macabre")

    with pytest.raises(ValueError):
        CExc(mock_subparser).run(None)

## END DEPRECATED

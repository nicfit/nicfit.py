import sys
import pytest
from deprecation import fail_if_not_removed
from unittest.mock import MagicMock as Mock
from nicfit.command import Command, CommandError, register


@pytest.fixture
def emptycommands2():
    Command._registered_commands.clear()


def test_loadCommandMap_Empty(emptycommands2):
    with pytest.raises(ValueError):
        Command.loadCommandMap(Mock())


def test_register(emptycommands2):
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


def test_dup_register(emptycommands2):
    @Command.register
    class c1(Command): pass # noqa

    @Command.register
    class c2(Command): pass # noqa

    with pytest.raises(ValueError):
        @Command.register
        class c2dup(Command):
            NAME = "c2"

    assert len(Command._registered_commands[Command]) == 2


def test_run_notimplemented(emptycommands2):
    @Command.register
    class TestCommand(Command):
        pass

    with pytest.raises(NotImplementedError):
        TestCommand().run(None)


def test_run(emptycommands2):
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
    cmd = Command.loadCommandMap(subparsers=mock_subparser)["test"]

    assert cmd.subparsers is mock_subparser
    assert cmd.parser is mock_parser
    cmd._initArgParser.assert_called_once_with(mock_parser)

    cmd.run(mock_args)
    if sys.version_info[:2] >= (3, 6):
        cmd._run.assert_called_once()
    else:
        assert cmd._run.call_count == 1
    assert cmd.args is mock_args
    mock_parser.set_defaults.assert_called_once_with(command_func=cmd.run)


def test_run_exit_status(emptycommands2):
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

## BEGIN DEPRECATED ##
@pytest.fixture
def emptycommands():
    Command._all_commands.clear()


def test_initAllEmpty_DEPRECATED(emptycommands):
    with pytest.raises(ValueError):
        Command.initAll(Mock())


def test_register_DEPRECATED(emptycommands):
    @register
    class c1(Command): pass # noqa

    @register
    class c2(Command): pass # noqa

    assert len(Command._all_commands) == 2
    Command.initAll(Mock(spec=["add_parser"]))


def test_dup_register_DEPRECATED(emptycommands):
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


def test_run_notimplemented_DEPRECATED(emptycommands):
    @register
    class TestCommand(Command):
        pass
    Command.initAll(Mock(spec=["add_parser"]))

    with pytest.raises(NotImplementedError):
        TestCommand(Mock()).run(None)


def test_run_DEPRECATED(emptycommands):
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
    if sys.version_info[:2] >= (3, 6):
        cmd._run.assert_called_once()
    else:
        assert cmd._run.call_count == 1
    assert cmd.args is mock_args
    mock_parser.set_defaults.assert_called_once_with(command_func=cmd.run)


def test_run_exit_status_DEPRECATED(emptycommands):
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

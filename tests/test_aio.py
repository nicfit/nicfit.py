import asyncio
import pytest
from unittest.mock import MagicMock as Mock
from nicfit import aio

def _assert_called_once(mocked):
    """Needed for pypy support even though nicfit.py support is 3.6 and above"""
    import sys
    if sys.version_info[:2] >= (3, 6):
        mocked.assert_called_once()
    else:
        assert mocked.call_count == 1


async def _main(args):
    args.app.retval = 2
    return 2

def atexit(app):
    app.atexit = 2


class Myapp(aio.Application):
    async def _main(self, args):
        assert args.app is self
        self.retval = 3
        return 3

    def _atexit(self):
        self.atexit = 3


def test_entryPoints():
    app = aio.Application(_main)
    with pytest.raises(SystemExit):
        app.run([])
    assert app.retval == 2

    app = Myapp()
    with pytest.raises(SystemExit):
        app.run([])
    assert app.retval == 3


def test_atexit(event_loop):
    app = aio.Application(atexit=atexit, event_loop=event_loop)
    with pytest.raises(SystemExit):
        app.run([])
    assert app.atexit == 2

    app = Myapp(event_loop=event_loop)
    with pytest.raises(SystemExit):
        app.run([])
    assert app.atexit == 3


def test_stop(event_loop):
    async def main(args):
        try:
            await asyncio.sleep(5, loop=event_loop)
        except asyncio.CancelledError:
            args.app.retval = 14
            raise
    app = aio.Application(main, event_loop=event_loop)

    def mgr():
        app.stop()
    event_loop.call_later(2, mgr)
    with pytest.raises(SystemExit):
        app.run([])
    assert app.retval == 14


def test_command(event_loop):
    with pytest.raises(NotImplementedError):
        event_loop.run_until_complete(aio.Command().run(None))

    class MyCommand(aio.Command):
        def __init__(self):
            self.was_run = False
        async def _run(self):
            self.was_run = True
            return 5

    cmd = MyCommand()
    assert not cmd.was_run
    dummy_args = object()
    res = event_loop.run_until_complete(cmd.run(dummy_args))
    assert cmd.args == dummy_args
    assert cmd.was_run
    assert res == 5


def test_subcommands(event_loop):
    run_body_mock2 = Mock()
    run_body_mock3 = Mock()

    class sub1(aio.Command):
        ...
    class sub2(aio.Command):
        async def _run(self):
            run_body_mock2()
    class sub3(aio.Command):
        async def _run(self):
            run_body_mock3()

    @aio.Command.register
    class TopLevelCommand(aio.SubCommandCommand):
        SUB_CMDS = [sub1, sub2, sub3]
        NAME = "top1"
        ALIASES = ["T", "t1"]

    @aio.Command.register
    class TopLevelCommand2(aio.SubCommandCommand):
        NAME = "top2"
        SUB_CMDS = [sub1, sub3]
        DEFAULT_CMD = sub3

    assert len(aio.Command._registered_commands[aio.Command]) == 4
    loaded = aio.Command.loadCommandMap()
    assert len(loaded) == 4

    assert id(loaded["top1"]) == id(loaded["T"]) == id(loaded["t1"])

    command = loaded["top1"]
    event_loop.run_until_complete(
        command.run(command.parser.parse_args(["sub2"])))
    _assert_called_once(run_body_mock2)

    command = loaded["top2"]
    event_loop.run_until_complete(command.run(command.parser.parse_args([])))
    _assert_called_once(run_body_mock3)

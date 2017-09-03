import asyncio
import pytest
from nicfit import aio


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

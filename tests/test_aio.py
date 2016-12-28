import asyncio
import pytest
from nicfit import aio


@asyncio.coroutine
def _main(args):
    args.app.retval = 2
    return 2

def atexit(app):
    app.atexit = 2


class Myapp(aio.Application):
    @asyncio.coroutine
    def _main(self, args):
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
    @asyncio.coroutine
    def main(args):
        try:
            yield from asyncio.sleep(5, loop=event_loop)
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

import pytest
import nicfit
from nicfit import aio

# XXX
pytestmark = pytest.mark.skipif(True, reason="fuckfcae")

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

def test_atexit():
    app = aio.Application(atexit=atexit)
    with pytest.raises(SystemExit):
        app.run()
    assert app.atexit == 2

    app = Myapp()
    with pytest.raises(SystemExit):
        app.run()
    assert app.atexit == 3


import pytest
import nicfit
try:
    with_curio = True
    import nicfit.curio
    from nicfit.curio import Application as CurioApp
except ImportError:
    with_curio = False
    CurioApp = object

pytestmark = pytest.mark.skipif(not with_curio, reason="curio not installed")

async def _main(args):
    args.app.retval = 2
    return 2

def atexit(app):
    app.atexit = 2

class Myapp(CurioApp):
    async def _main(self, args):
        assert args.app is self
        self.retval = 3
        return 3
    def _atexit(self):
        self.atexit = 3


def test_entryPoints():
    app = nicfit.curio.Application(_main)
    with pytest.raises(SystemExit):
        app.run([])
    assert app.retval == 2

    app = Myapp()
    with pytest.raises(SystemExit):
        app.run([])
    assert app.retval == 3

def test_atexit():
    app = nicfit.curio.Application(atexit=atexit)
    with pytest.raises(SystemExit):
        app.run()
    assert app.atexit == 2

    app = Myapp()
    with pytest.raises(SystemExit):
        app.run()
    assert app.atexit == 3

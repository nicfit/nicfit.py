import nicfit
from nicfit.app import Application, AsyncApplication
import pytest


def _main(args):
    args.app.retval = 2
    return 2

def atexit(app):
    app.atexit = 2

class Myapp(Application):
    def _main(self, args):
        assert args.app is self
        self.retval = 3
        return 3
    def _atexit(self):
        self.atexit = 3


def test_entryPoints():
    app = Application(_main)
    with pytest.raises(SystemExit):
        app.run([])
    assert app.retval == 2

    app = Myapp()
    with pytest.raises(SystemExit):
        app.run([])
    assert app.retval == 3


def test_atexit():
    app = Application(atexit=atexit)
    with pytest.raises(SystemExit):
        app.run()
    assert app.atexit == 2

    app = Myapp()
    with pytest.raises(SystemExit):
        app.run()
    assert app.atexit == 3

def test_nomain():
    app = Application()
    assert app.main([]) == Application.NO_MAIN_EXIT

def test_AsyncApp():
    app = AsyncApplication()
    with pytest.raises(NotImplementedError):
        app._run([])

# FIXME: how to test await main

import sys
import pytest
from unittest.mock import patch, Mock
import nicfit.app
from nicfit.app import Application, AsyncApplication


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


def test_unhandled():
    def m(args):
        args.app.retval = Application.UNCAUGHT_EXCEPTION_EXIT
        raise ValueError("1969")
    app = Application(m)
    with pytest.raises(SystemExit):
        app.run([])
    assert app.retval == Application.UNCAUGHT_EXCEPTION_EXIT


def test_version(capfd):
    app = Application(version="6.6.6")
    with pytest.raises(SystemExit):
        app.run(["--version"])
    out, _ = capfd.readouterr()
    assert out.strip() == "6.6.6"


def test_pdb():
    app = Application(pdb_opt=True)
    app._main = Mock(side_effect=ValueError)

    with patch.object(nicfit.util._debugger, "post_mortem") as mock_pm:
        try:
            app.run(["--pdb"])
        except SystemExit:
            if sys.version_info[:2] >= (3, 6):
                mock_pm.assert_called()
            else:
                assert mock_pm.call_count != 0
        else:
            pytest.fail("Expected ValueError")

##
# AsyncApplication tests
##

def test_AsyncApp():
    app = AsyncApplication()
    with pytest.raises(NotImplementedError):
        app._run([])


async def _asyncMain(args):
    args.app.reval = 10
    return 10


@pytest.mark.asyncio
async def test_async_main():
    app = AsyncApplication()
    assert await app._main(None) == AsyncApplication.NO_MAIN_EXIT


@pytest.mark.asyncio
async def test_async_mainFunc():
    app = AsyncApplication(_asyncMain)
    assert await app.main([]) == 10

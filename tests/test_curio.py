import pytest
import nicfit
try:
    with_curio = True
    import nicfit.curio
except ImportError:
    with_curio = False

# XXX
pytestmark = pytest.mark.skipif(True, reason="FIXME")
#pytestmark = pytest.mark.skipif(not with_curio, reason="curio not installed")

if with_curio:
    async def _main(args):
        args.app.retval = 2
        return 2

    def atexit(app):
        app.atexit = 2

    class Myapp(nicfit.curio.Application):
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

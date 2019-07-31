import os
import sys
import pytest
from unittest.mock import patch, Mock
from nicfit.app import Application
from nicfit.__main__ import app, Nicfit
from nicfit.console.ansi import Fg, Style


def test_NicfitApp_default(capfd):
    with pytest.raises(SystemExit):
        app.run([])
    out, err = capfd.readouterr()
    assert out == Fg.red("\\m/ {} \\m/".format(Style.inverse("Welcome"))) + "\n"


@pytest.mark.skipif("TRAVIS" in os.environ,
                    reason="Failing on Travis-CI only, not finding msg catalog "
                           "now, was before :/")
def test_NicfitApp_español(capfd):
    lang = os.environ["LANG"] if "LANG" in os.environ else None
    with pytest.raises(SystemExit):
        os.environ["LANG"] = "es"
        Nicfit().run([])

    out, err = capfd.readouterr()
    assert out == Fg.red("\\m/ {} \\m/"
                         .format(Style.inverse("Bienvenido"))) + "\n"

    os.environ["LANG"] = lang


def test_NicfitApp_invalid():
    with pytest.raises(SystemExit) as ex:
        app.run(["Side By Side"])
    assert ex.value.code == 2


def test_NicfitApp_cookiecutter_None(tmpdir):
    with patch("nicfit.__main__.cookiecutter", None):
        with pytest.raises(SystemExit) as sysexit:
            app.run(["cookiecutter", str(tmpdir)])
        assert sysexit.value.code == 1


def test_NicfitApp_cookiecutter_mock(tmpdir):
    mock_cc = Mock()
    with patch("nicfit.__main__.cookiecutter", mock_cc):
        with pytest.raises(SystemExit) as sysexit:
            app.run(["cookiecutter", "--no-clone", str(tmpdir)])

        assert sysexit.value.code == 0
        if sys.version_info[:2] >= (3, 6):
            mock_cc.assert_called_once()
        else:
            assert mock_cc.call_count == 1
        # XXX: is there "any matcher" in pytest?
        args, kwargs = mock_cc.call_args
        assert kwargs["output_dir"] == str(tmpdir)


def test_NicfitApp_cookiecutter_exception(tmpdir):
    from cookiecutter.exceptions import CookiecutterException
    mock_cc = Mock(side_effect=CookiecutterException)
    with patch("nicfit.__main__.cookiecutter", mock_cc):
        with pytest.raises(SystemExit) as sysexit:
            app.run(["cookiecutter", str(tmpdir)])
        assert sysexit.value.code == 1


@pytest.mark.skipif("TRAVIS" in os.environ,
                    reason="Failing on Travis-CI only, unshallowed_repo not "
                           "working.")
def test_NicfitApp_cookiecutter_real(tmpdir, unshallowed_repo):
    with pytest.raises(SystemExit) as sysexit:
        app.run(["cookiecutter", str(tmpdir), "--no-input"])
    assert sysexit.value.code == 0
    # XXX: validate the results?


def test_commands_noargs_notrequired():
    class MyApp(Application):
        def _main(self, args):
            return 0

    app = MyApp()
    app.arg_parser.add_subparsers(required=False, dest="cmd")
    try:
        app.run([])
    except SystemExit as exit:
        assert exit.code == 0
    else:
        assert False, "App did not invoke sys.exit"


def test_commands_noargs_required():
    class MyApp(Application):
        def _main(self, args):
            return 0

    app = MyApp()
    app.arg_parser.add_subparsers(required=True, dest="cmd")
    try:
        app.run([])
    except SystemExit as exit:
        assert exit.code == 2
    else:
        assert False, "App did not invoke sys.exit"

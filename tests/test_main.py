# -*- coding: utf-8 -*-
import sys
import pytest
from unittest.mock import patch, Mock
from nicfit.__main__ import app
from nicfit.console.ansi import Fg, Style


def test_NicfitApp_default(capfd):
    with pytest.raises(SystemExit):
        app.run([])
    out, _ = capfd.readouterr()
    assert out == Fg.red("\m/ {} \m/".format(Style.inverse("Listen to more Slayer"))) + "\n"


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
    import nicfit
    mock_cc = Mock(side_effect=nicfit.__main__.CookiecutterException)
    with patch("nicfit.__main__.cookiecutter", mock_cc):
        with pytest.raises(SystemExit) as sysexit:
            app.run(["cookiecutter", str(tmpdir)])
        assert sysexit.value.code == 1


@pytest.mark.skip(reason="Failing on Travis-CI only, most likely to env diffs")
def test_NicfitApp_cookiecutter_real(tmpdir, unshallowed_repo):
    with pytest.raises(SystemExit) as sysexit:
        app.run(["cookiecutter", str(tmpdir), "--no-input"])
    assert sysexit.value.code == 0
    # XXX: validate the results?

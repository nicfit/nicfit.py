import os
import nicfit.util


def test_cd():
    cwd = os.getcwd()
    with nicfit.util.cd("/tmp"):
        assert os.getcwd() == "/tmp"
    assert os.getcwd() == cwd

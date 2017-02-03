from nicfit.console import pout, perr, ansi


"""
def test_pouterr2(capfd):
    print("hi")
    out, err = capfd.readouterr()
    assert out == "hi" + "\n"
"""


def test_pout(capsys):
    msg = "There's a war outside!"
    pout(msg)
    out, _ = capsys.readouterr()
    assert out == msg + "\n"


def test_perr(capsys):
    msg = "There's a war outside!"
    perr(msg)
    _, err = capsys.readouterr()
    assert err == msg + "\n"

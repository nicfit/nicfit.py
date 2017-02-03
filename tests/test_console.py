import os
import types
import logging
from unittest.mock import patch
import pytest
from nicfit.console import pout, perr
from nicfit.console.ansi import Fg, Bg, Style, init as ansi_init
import contextlib


@contextlib.contextmanager
def envvars(*vars):
    saved = {}
    for v in vars:
        saved[v] = os.environ[v] if v in os.environ else None
    try:
        yield
    finally:
        for v in saved:
            if saved[v]:
                os.environ[v] = saved[v]
            elif v in os.environ:
                del os.environ[v]


def test_pout(capfd):
    msg = "There's a war outside!"
    pout(msg)
    out, _ = capfd.readouterr()
    assert out == msg + "\n"


def test_perr(capfd):
    msg = "There's a war outside!"
    perr(msg)
    _, err = capfd.readouterr()
    assert err == msg + "\n"


def test_plog(capfd):
    msg = "Xymox - Phoenix"

    log = logging.getLogger("test_plog")
    with patch.object(log, "info") as mock:
        pout(msg, log=log)
    out, _ = capfd.readouterr()
    assert out == msg + "\n"
    mock.assert_called_once_with(msg)


def test_ansi_unsupported():
    with envvars("TERM", "OS"):
        for var, invalids in [("TERM", ["dumb"]), ("OS", ["Windows_NT"])]:
            for val in invalids:
                os.environ[var] = val
                with pytest.raises(ValueError):
                    ansi_init(True)


def test_ansi():
    CSI = "\033["

    class KnownFg:
        (GREY,
         RED,
         GREEN,
         YELLOW,
         BLUE,
         MAGENTA,
         CYAN,
         WHITE) = [*range(30, 38)]
        RESET = 39

    class KnownBg:
        (GREY,
         RED,
         GREEN,
         YELLOW,
         BLUE,
         MAGENTA,
         CYAN,
         WHITE) = [*range(40, 48)]
        RESET = 49

    class KnownStyle:
        (RESET_ALL,
         BRIGHT,
         DIM,
         ITALICS,
         UNDERLINE,
         BLINK_SLOW,
         BLINK_FAST,
         INVERSE) = [*range(0, 8)]
        STRIKE_THRU = 9
        (RESET_BRIGHT,
         RESET_ITALICS,
         RESET_UNDERLINE,
         RESET_BLINK_SLOW,
         RESET_BLINK_FAST,
         RESET_INVERSE) = [*range(22, 28)]
        RESET_STRIKE_THRU = 29
        RESET_DIM = RESET_BRIGHT

    def mkcode(c):
        return "{}{}m".format(CSI, c)

    ansi_init(True)

    for known_palette, palette in ((KnownFg, Fg),
                                   (KnownBg, Bg),
                                   (KnownStyle, Style),
                                  ):
        code_list = [c for c in dir(known_palette) if c == c.upper()]

        # Test values and members
        if known_palette in (KnownFg, KnownBg):
            assert len(code_list) == 9
        else:
            assert len(code_list) == 17

        for c in code_list:
            assert type(getattr(palette, c)) is str
            assert mkcode(getattr(known_palette, c)) == \
                getattr(palette, c)
            if palette is Style and c.lower().startswith("reset_"):
                # Style.reset_*() functions don't exist
                continue

            assert isinstance(getattr(palette, c.lower()), types.FunctionType)

            # Test palette functions vs codes
            assert Fg.BLUE + "SNFU" + Fg.RESET == Fg.blue("SNFU")

            code = getattr(palette, c)
            if palette is Style:
                reset = getattr(palette, "RESET_{}".format(c))
            else:
                reset = getattr(palette, "RESET")
            func = getattr(palette, c.lower())

            assert code + "SNFU" + reset == func("SNFU")


def test_ansi_palette_attr_disabled():
    ansi_init(False)
    for palette in (Fg, Bg, Style):
        code_list = [c for c in dir(palette) if c == c.upper()]

        for c in code_list:
            assert getattr(palette, c) == ""


def test_ansi_formats():
    ansi_init(True)

    s = "Heavy Cream - Run Free"
    assert Fg.green(s, Style.BRIGHT,
                       Style.UNDERLINE,
                       Style.ITALICS) == \
           Style.BRIGHT + Style.UNDERLINE + Style.ITALICS + Fg.GREEN + s + \
           Fg.RESET + Style.RESET_ALL

    print("%(BLUE)sNice%(RESET)s" % Fg)

    # TODO: More complex examples and future format schems

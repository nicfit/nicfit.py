import os
import sys

_USE_ANSI = False


def init(enabled=os.isatty(sys.stdout.fileno())):
    global _USE_ANSI

    if enabled and (("TERM" in os.environ and os.environ["TERM"] == "dumb") or
                    ("OS" in os.environ and os.environ["OS"] == "Windows_NT")):
        raise ValueError("ANSI not suported on dumb terminals or Windows")
    else:
        _USE_ANSI = enabled


class FgPalette:
    (GREY,
     RED,
     GREEN,
     YELLOW,
     BLUE,
     MAGENTA,
     CYAN,
     WHITE) = [*range(30, 38)]
    RESET = 39


class BgPalette:
    (GREY,
     RED,
     GREEN,
     YELLOW,
     BLUE,
     MAGENTA,
     CYAN,
     WHITE) = [*range(40, 48)]
    RESET = 49


class StylePalette:
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


class AnsiCodes(object):
    _CSI = "\033["

    def __init__(self, codes):
        def code_to_chars(code):
            return AnsiCodes._CSI + str(code) + 'm'

        for name in dir(codes):
            if name == name.upper():
                value = getattr(codes, name)
                setattr(self, name, code_to_chars(value))

                # Add color function
                for reset_name in ("RESET_%s" % name, "RESET"):
                    if hasattr(codes, reset_name):
                        reset_value = getattr(codes, reset_name)
                        setattr(self, "%s" % name.lower(),
                                AnsiCodes._mkfunc(code_to_chars(value),
                                                  code_to_chars(reset_value)))
                        break

    @staticmethod
    def _mkfunc(color, reset):
        def _cwrap(text, *styles):
            if not _USE_ANSI:
                return text

            s = u""
            for st in styles:
                s += st
            s += color + text + reset
            if styles:
                s += Style.RESET_ALL
            return s
        return _cwrap

    def __getattribute__(self, name):
        attr = super(AnsiCodes, self).__getattribute__(name)
        if (hasattr(attr, "startswith") and
                attr.startswith(AnsiCodes._CSI) and
                not _USE_ANSI):
            return ""
        else:
            return attr

    def __getitem__(self, name):
        return getattr(self, name.upper())


Fg = AnsiCodes(FgPalette)
Bg = AnsiCodes(BgPalette)
Style = AnsiCodes(StylePalette)

r"""

Examples:
---------
::

    from nicfit.console.ansi import init, Fg, Bg, Style

    ansi.init(True)

    print(Fg.RED + "\m/ \m/" + Fg.RESET)
    print(Style.BRIGHT + Fg.RED + "\m/ \m/" + Fg.RESET)
    print(Fg.blue("\m/ \m/"))
    print(Style.BLINK_SLOW + Fg.green("\m/ \m/"))
    print(Style.DIM + Fg.green("\m/ \m/"))
    print(Fg.yellow("\m/ \m/", Style.BRIGHT, Style.UNDERLINE, Style.ITALICS))
    print("{b}\{g}m{r}{b}/{r}".format(b=Fg.BLUE, g=Fg.GREEN, r=Fg.RESET))
    print(Bg.green(Fg.yellow("\{}/".format(Style.strike_thru("mmmm")))))
    print("%(BLUE)sNice%(RESET)s" % Fg)

    # TODO
    ################################################################################
"""

__all__ = ["Fg", "Bg", "Style"]

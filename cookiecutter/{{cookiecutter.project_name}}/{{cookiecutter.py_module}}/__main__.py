# -*- coding: utf-8 -*-
from nicfit import Application
from . import __version__


def main(args):
    print("\m/")


app = Application(main, version=__version__)
if __name__ == "__main__":
    app.run()

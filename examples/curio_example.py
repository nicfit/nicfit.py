#!/usr/bin/env python
import time
from nicfit.curio import Application

async def _main(args):
    print(args)
    time.sleep(2)
    return 0

def atexit():
    print("atexit")


app = Application(_main, atexit=atexit)
app.arg_parser.add_argument("--example", help="Example cli")
app.run()
assert not"will not execute"

#!/usr/bin/env python
import time
from nicfit.aio import Application

async def _main(args):
    print(args)
    print("Sleeping 2...")
    time.sleep(2)
    print("Sleeping 0...")
    return 0

def atexit():
    print("atexit")


app = Application(_main, atexit=atexit)
app.arg_parser.add_argument("--example", help="Example cli")
app.run()
assert not"will not execute"

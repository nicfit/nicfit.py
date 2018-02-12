#!/usr/bin/env python
import time
import nicfit

def main(args):
    print("Parsed command line args:", args)
    try:
        print("Sleeping 5, Ctrl-C to interupt...")
        time.sleep(10)
    except KeyboardInterrupt:
        print("Returning 2...")
        return 2
    else:
        print("Returning 0...")
        return 0

def atexit():
    print("atexit, in case you care")


app = nicfit.Application(main, name="example", description="Just an example",
                         version="1.0a0", atexit=atexit, pdb_opt=True)
app.arg_parser.add_argument("--example", help="Example cli")
app.run()
assert not"will not execute"

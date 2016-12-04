import nicfit

def _main(args):
    import time
    print(args)
    time.sleep(15)
    return 0

def atexit():
    print("atexit")


app = nicfit.Application(_main, atexit=atexit)
app.arg_parser.add_argument("--example", help="Example cli")
app.run()
assert not"will not execute"

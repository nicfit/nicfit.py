import nicfit
from nicfit.curio import Application

async def _main(args):
    import time
    print(args)
    time.sleep(5)
    return 5

def atexit():
    print("atexit")


app = Application(_main, atexit=atexit)
app.arg_parser.add_argument("--example", help="Example cli")
app.run()
assert not"will not execute"

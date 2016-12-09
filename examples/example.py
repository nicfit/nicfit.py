import time
import nicfit

def main(args):
    print(args)
    try:
        time.sleep(15)
    except KeyboardInterrupt:
        raise ValueError()
        return 1
    else:
        return 0

def atexit():
    print("in case you care")


app = nicfit.Application(main, name="example", description="Just an example",
                         version="1.0.0-alpha",
                         atexit=atexit, pdb_opt=True)
app.arg_parser.add_argument("--example", help="Example cli")
app.run()
assert not"will not execute"

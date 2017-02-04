#!/usr/bin/env python
import sys
import json
from pathlib import Path


def write_cc_yaml(cc_json, pre_template):
    with open(str(cc_json)) as fp:
        data = json.loads(fp.read())

    with open(str(pre_template)) as fp:
        line = fp.readline()
        while line:
            if line.strip() != "@USER_CONFIG@":
                print(line.rstrip())
            else:
                print("default_context:")
                for k in sorted(data.keys()):
                    if not k.startswith("_"):
                        val = data[k]
                        if isinstance(val, list):
                            val = val[0]
                        print("{ident}{key}: \"{{{{ cookiecutter.{key} }}}}\""
                              .format(ident=" " * 4, key=k))
            line = fp.readline()


if __name__ == "__main__":
    cc_json = sys.argv[1]
    pre_template = sys.argv[2]
    write_cc_yaml(Path(cc_json), Path(pre_template))

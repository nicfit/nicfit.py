# -*- coding: utf-8 -*-
import sys
import types

PY2 = sys.version_info[0] == 2
PY26 = sys.version_info[0:2] == (2, 6)

if not PY2:
    # Python 3

    StringTypes = (str,)
    UnicodeType = str
    BytesType = bytes
    unicode = str

    from io import StringIO

else:
    # Python 2

    StringTypes = types.StringTypes
    UnicodeType = unicode
    BytesType = str
    unicode = unicode

    from StringIO import StringIO



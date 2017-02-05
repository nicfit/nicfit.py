# -*- coding: utf-8 -*-
import pytest
from pathlib import Path


@pytest.fixture
def unshallowed_repo():
    from nicfit.console import perr
    src = "./.git/shallow_file"
    bak = src + ".BACKUP"

    shallow_file = Path(src)
    perr("$EXISTS: " + str(shallow_file.exists()))
    if shallow_file.exists():
        shallow_file.rename(bak)
        perr("$BEFORE: " + str(list(shallow_file.parent.iterdir())))
        yield shallow_file
        shallow_file = Path(bak).rename(src)
        perr("$AFTER: " + str(list(shallow_file.parent.iterdir())))
    else:
        yield None

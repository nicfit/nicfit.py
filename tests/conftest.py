# -*- coding: utf-8 -*-
import pytest
from pathlib import Path


@pytest.fixture
def unshallowed_repo():
    src = "./.git/shallow"
    bak = src + ".BACKUP"

    shallow_file = Path(src)
    if shallow_file.exists():
        shallow_file.rename(bak)
        yield shallow_file
        shallow_file = Path(bak).rename(src)
    else:
        yield None

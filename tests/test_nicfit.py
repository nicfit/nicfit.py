# -*- coding: utf-8 -*-
import pytest
import nicfit
"""
test_nicfit
----------------------------------

Tests for `nicfit` module.
"""


def test_metadata():
    assert nicfit.version
    assert nicfit.__about__.__license__
    assert nicfit.__about__.__project_name__
    assert nicfit.__about__.__author__
    assert nicfit.__about__.__author_email__
    assert nicfit.__about__.__version__
    assert nicfit.__about__.__version_info__
    assert nicfit.__about__.__release__
    assert nicfit.__about__.__version_txt__


def test_parse_version():
    from nicfit.__about__ import __parse_version
    assert __parse_version("0") == ("0", "final", (0, 0, 0, "final"))
    assert __parse_version("1a1") == ("1", "a1", (1, 0, 0, "a1"))
    assert __parse_version("1.2b1") == ("1.2", "b1", (1, 2, 0, "b1"))
    assert __parse_version("1.2.3c1") == ("1.2.3", "c1", (1, 2, 3, "c1"))
    assert __parse_version("2.0") == ("2.0", "final", (2, 0, 0, "final"))

    for invalid in ["3.0.3d1", "a.b.c"]:
        with pytest.raises(ValueError):
            __parse_version(invalid)

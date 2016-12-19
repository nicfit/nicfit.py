# -*- coding: utf-8 -*-
import nicfit
"""
test_nicfit
----------------------------------

Tests for `nicfit` module.
"""


def test_metadata():
    assert nicfit.__license__
    assert nicfit.__project_name__
    assert nicfit.__author__
    assert nicfit.__author_email__
    assert nicfit.__version__
    assert nicfit.__version_info__
    assert nicfit.__release__
    assert nicfit.__version_txt__

# -*- coding: utf-8 -*-
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

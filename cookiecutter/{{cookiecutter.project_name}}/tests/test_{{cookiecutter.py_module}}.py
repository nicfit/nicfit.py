# -*- coding: utf-8 -*-
import pytest
import {{ cookiecutter.py_module }}
"""
test_{{ cookiecutter.py_module }}
----------------------------------

Tests for `{{ cookiecutter.py_module }}` module.
"""


def test_metadata():
    assert {{ cookiecutter.py_module }}.version
    assert {{ cookiecutter.py_module }}.__about__.__license__
    assert {{ cookiecutter.py_module }}.__about__.__project_name__
    assert {{ cookiecutter.py_module }}.__about__.__author__
    assert {{ cookiecutter.py_module }}.__about__.__author_email__
    assert {{ cookiecutter.py_module }}.__about__.__version__
    assert {{ cookiecutter.py_module }}.__about__.__version_info__
    assert {{ cookiecutter.py_module }}.__about__.__release__
    assert {{ cookiecutter.py_module }}.__about__.__version_txt__

# -*- coding: utf-8 -*-
{% if cookiecutter.use_pytest == "yes" -%}
import pytest
{%- else -%}
import unittest
from nose.tools import *
{% endif %}
import {{ cookiecutter.py_module }}
"""
test_{{ cookiecutter.py_module }}
----------------------------------

Tests for `{{ cookiecutter.py_module }}` module.
"""

{% if cookiecutter.use_pytest != "yes" -%}
class Test{{ cookiecutter.py_module|capitalize }}(unittest.TestCase):

    def setUp(self):
        pass

    def test_metadata(self):
        assert({{ cookiecutter.py_module }}.__name__)
        assert({{ cookiecutter.py_module }}.__author__)
        assert({{ cookiecutter.py_module }}.__author_email__)
        assert({{ cookiecutter.py_module }}.__version__)
        assert({{ cookiecutter.py_module }}.__version_info__)
        assert({{ cookiecutter.py_module }}.__release__)
        assert({{ cookiecutter.py_module }}.__license__)
        assert({{ cookiecutter.py_module }}.__version_txt__)

    def tearDown(self):
        pass


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
{%- else -%}
def test_metadata():
    assert {{ cookiecutter.py_module }}.__license__
    assert {{ cookiecutter.py_module }}.__project_name__
    assert {{ cookiecutter.py_module }}.__author__
    assert {{ cookiecutter.py_module }}.__author_email__
    assert {{ cookiecutter.py_module }}.__version__
    assert {{ cookiecutter.py_module }}.__version_info__
    assert {{ cookiecutter.py_module }}.__release__
    assert {{ cookiecutter.py_module }}.__version_txt__
{% endif %}

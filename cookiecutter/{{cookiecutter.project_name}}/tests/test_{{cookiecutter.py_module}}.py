# -*- coding: utf-8 -*-

"""
test_{{ cookiecutter.project_slug }}
----------------------------------

Tests for `{{ cookiecutter.project_slug }}` module.
"""

{% if cookiecutter.use_pytest == "yes" -%}
import pytest
{%- else -%}
import unittest
from nose.tools import *
{% endif %}
import {{ cookiecutter.project_slug }}
{% if cookiecutter.use_pytest != "yes" -%}


class Test{{ cookiecutter.project_slug|capitalize }}(unittest.TestCase):

    def setUp(self):
        pass

    def test_metadata(self):
        assert({{ cookiecutter.project_slug }}.__name__)
        assert({{ cookiecutter.project_slug }}.__author__)
        assert({{ cookiecutter.project_slug }}.__author_email__)
        assert({{ cookiecutter.project_slug }}.__version__)
        assert({{ cookiecutter.project_slug }}.__version_info__)
        assert({{ cookiecutter.project_slug }}.__release__)
        assert({{ cookiecutter.project_slug }}.__license__)
        assert({{ cookiecutter.project_slug }}.__version_txt__)

    def tearDown(self):
        pass


if __name__ == '__main__':
    import sys
    sys.exit(unittest.main())
{% endif %}

# -*- coding: utf-8 -*-
{%- if cookiecutter.pyapp_type == "asyncio" -%}
{%- set async = "async" -%}
{%- set appmod = "nicfit.aio" -%}
{%- else -%}
{%- set async = "" -%}
{%- set appmod = "nicfit" -%}
{%- endif %}
from {{ appmod }} import Application
from nicfit.console import pout
from . import version


{{ async }} def main(args):
    pout("\m/")


app = Application(main, version=version,
{%- if cookiecutter.gettext_domain != "None" %}
                  gettext_domain="{{ cookiecutter.gettext_domain }}")
{% else %}
                  gettext_domain=None)
{% endif %}
if __name__ == "__main__":
    app.run()

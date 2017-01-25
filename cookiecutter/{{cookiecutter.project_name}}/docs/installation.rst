============
Installation
============

Using pip
------------
At the command line::

    $ pip install {{ cookiecutter.project_slug }}

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv {{ cookiecutter.project_name }}
    $ pip install {{ cookiecutter.project_slug }}

Using a source distribution
-----------------------------
At the command line:

.. parsed-literal::

    $ tar zxf {{ cookiecutter.project_slug }}-|version|.tar.gz
    $ cd {{ cookiecutter.project_slug }}-|version|
    $ python setup.py install

{%- if cookiecutter.use_github == "yes" %}
From GitHub
{%- else %}
From BitBucket
{%- endif %}
--------------
At the command line::

{%- if cookiecutter.use_github == "yes" %}
    $ git clone {{ cookiecutter.github_url }}
{%- else %}
    $ hg clone {{ cookiecutter.bitbucket_url }}
{%- endif %}
    $ cd mishmash
    $ python setup.py install

Additional dependencies should be installed if developing MishMash::

    $ pip install -r requirements/dev.txt

Dependencies
-------------
All the required software dependencies are installed using either
``requirements/default.txt`` files or by ``python install setup.py``.

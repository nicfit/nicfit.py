nicfit.Application
-------------------

.. image:: https://badge.fury.io/py/nicfit.py.svg
    :target: http://badge.fury.io/py/nicfit.py

.. image:: https://travis-ci.org/nicfit/nicfit.py.png?branch=master
        :target: https://travis-ci.org/nicfit/nicfit.py

.. image:: https://img.shields.io/travis/nicfit/nicfit.py.svg
        :target: https://travis-ci.org/nicfit/nicfit.py

.. image:: https://img.shields.io/pypi/v/nicfit.py.svg
        :target: https://pypi.python.org/pypi/nicfit.py


Common Python utils (App, logging, config, etc.)

* Free software: MIT license
* Documentation: https://nicfit.py.readthedocs.org.

Features
--

.. code-block:: python

    from nicfit import Application
    def main(args):
        return 0
     app = Application(main)
     app.run()


What you get:

- An ArgumentParser (app.arg_parser)
- Logger (app.log)
- Top-level exception handling (e.g. KeyboardInterrupt, uncaught exception
  logging)
- Reliable sys.exit return codes.

Maybe you don't what to ``sys.exit``.

.. code-block:: python

    retval = app.main()

 What you lose:

 - sys.exit
 - Top-level exception handling

Invoke code right before ``sys.exit``.

.. code-block:: python

    def f(): pass
    app = Application(main, atexit=f)


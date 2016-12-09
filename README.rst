nicfit.Application
-------------------
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

Release procedure
~~~~~~~~~~~~~~~~~~~
::
    make pre-release
    make release
    make PYPI_REPO=pypi upload-release

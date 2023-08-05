*************************
AX Semantics Sphinx Theme
*************************

This is a fork of the `sphinx_rtd_theme <https://sphinx-rtd-theme.readthedocs.io/en/latest/index.html>`
by readthedocs.org_. It removes a lot of styling and all javascript, and adds a configuration option
to include a header row with links.

.. _readthedocs.org: http://www.readthedocs.org


Installing
==========

The theme is distributed on PyPI_ and can be installed with pip::

   pip install axsemantics_sphinx_theme

.. _PyPI: https://pypi.python.org/pypi/axsemantics_sphinx_theme


Configuration
=============

tbd

Release workflow
================

Releasing a new version requires the developer to bump the version in ``__init__.py``, commit and tag the changes, and then run::

    $ rm -rf dist/
    $ python setup.py sdist bdist_wheel
    $ twine upload dist/*

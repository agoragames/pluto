pluto
=====

:Version: 0.0.1
:Download: http://pypi.python.org/pypi/pluto
:Source: https://github.com/agoragames/pluto
:Keywords: python, analytics, celery

.. contents::
    :local:

Overview
========

Pluto provides a set of tools and standards around developing analytics engines.

Installation
============

During the initial stage of development, ``pluto`` is only available from GitHub.

.. _chai-installing-from-git:

Using the development version
-----------------------------

You can clone the repository by doing the following::

    $ git clone git://github.com/agoragames/pluto.git
    $ cd pluto
    $ pip install -r development.pip

Execution
=========

To run the celery worker using predefined worker parameters: ::

    $ celery worker --config pluto.celeryconfig

Tests
=====

Use `nose <https://github.com/nose-devs/nose/>`_ to run the test suite. ::

  $ nosetests

The tests require a local MongoDB instance running on the standard port.

License
=======

This software is licensed under the `MIT License`. See the ``LICENSE.txt``
file in the top distribution directory for the full license text.

.. # vim: syntax=rst expandtab tabstop=4 shiftwidth=4 shiftround

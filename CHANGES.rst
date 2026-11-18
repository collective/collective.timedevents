Changelog
=========

2.0.0 (2026-11-18)
------------------

Breaking changes:

- Native namespace package (PEP 420): ``collective/__init__.py`` is gone.
  Plone 6.1 on Python 3.10 to 3.13, and Plone 6.2 on Python 3.10 to 3.14,
  only. Applications on Python 2 or older Plone releases must stay on 1.1.
  [bsuttor]

New features:

- Use ``importlib.metadata`` instead of ``pkg_resources``, which setuptools 81+
  deprecates and setuptools 84 (Plone 6.2.3) no longer ships.
  [bsuttor]

Internal:

- Configure with plone.meta: tox test matrix (Plone 6.2.3 on Python 3.10 to
  3.14, Plone 6.1 on Python 3.10 to 3.13), GitHub Actions, pre-commit. Package
  metadata moved to ``pyproject.toml``, ``src/`` layout, ``plone.autoinclude``
  entry point.
  [bsuttor]

- ``make install`` builds a uv development environment on Plone 6.2.3.
  Travis, buildout configuration and the hand-written GitHub workflow are gone.
  [bsuttor]


1.1 (2021-08-26)
----------------

- Add Python 3 & Plone 5.2 compatibility
  [boulch]

- Use github CI for automated testing
  [tomgross]


1.0.3 (2016-02-01)
------------------

- One final attempt to include HISTORY.txt into egg
  [tomgross]


1.0.2 (2016-02-01)
------------------

- Fix brown bag release part 2
  [tomgross]

1.0.1 (2016-02-01)
------------------

- Fix brown bag release
  [tomgross]


1.0 (2016-01-30)
----------------

- Plone 5 compatibility
  [karalics, tomgross]


0.3 (2013-12-14)
----------------

* Travis CI integration
  [hvelarde]

* Added cron-style tick events, to be triggered by cron or clockserver, with no internal calculation of interval. Updated readme and tests.
  [sunew]

0.2.1 (2012-04-24)
------------------

* Added logging level option for tick_logger
  [vmaksymiv]
* Bugfix: data storage

0.2
----------------

* Added Plone 4 compatibility
  [kroman0]

0.1.1 (2008-11-04)
------------------

* PyPi egg fixes

0.1
----------------

* Initial release


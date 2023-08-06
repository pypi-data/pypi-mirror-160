#########
Ratio ESL
#########

Ratio support for the  Elephant Specification Language (ESL) in Python.


**********
Quickstart
**********

Installation
============

RaESL can be installed using ``pip install raesl`` for any Python version >=3.9. Or,
for Poetry managed projects, use ``poetry add raesl`` to add it as a dependency.

For RaESL's different subcommands and functionality, the wheel provides extras:

* doc: documentation generation using pandoc, Markdown and optionally LaTeX.
* jupyter: a Jupyter ESL kernel.
* pygments: an ESL syntax highlighter for pygments.
* rich: Rich doc output in the form of Plotly images.
* server: A language server to parse documents.


The default ``compile`` command is always available.

Please refer to the `usage documentation <https://raesl.ratio-case.nl>`_ for more info
on how to use RaESL.


***************
Developer guide
***************

Python packaging information
============================

This project is packaged using `poetry <https://python-poetry.org/>`_. Packaging
information as well as dependencies are stored in `pyproject.toml <./pyproject.toml>`_.

Installing the project and its development dependencies can be done using ``poetry install``.


Invoke tasks
============

Most elemental maintenance tasks can be accomplished using
[Invoke](https://www.pyinvoke.org/). After installing using ``poetry install`` and
enabling the environment using ``poetry shell``, you can run all tasks using ``inv
[taskname]`` or ``invoke [taskname]``. E.g. ``inv docs`` builds the documentation.


Versioning
==========

This project uses `semantic versioning <https://semver.org>`_. Version increments are
checked using `Raver <https://raver.ratio-case.nl>`_.


Changelog
=========

Changelog format as described by https://keepachangelog.com/ has been adopted.

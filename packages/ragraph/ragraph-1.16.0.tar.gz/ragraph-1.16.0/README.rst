#######
RaGraph
#######

RaGraph is a package to create, manipulate, and analyze graphs consisting of nodes and
edges. Nodes usually represent (hierarchies of) objects and edges the dependencies or
relationships between them.

These graphs, or networks if you will, lend themselves well to applied analyses like
clustering and sequencing, as well as analyses involving the calculation of various
insightful metrics.


**********
Quickstart
**********

Installation
============

RaGraph can be installed using ``pip install ragraph`` for any Python version >=3.9. Or,
for Poetry managed projects, use ``poetry add ragraph`` to add it as a dependency.


Using RaGraph
=============

RaGraph's primary use is working with Graph objects that contain Nodes and Eges between
Nodes. See the `usage documentation <https://ragraph.ratio-case.nl/usage/index.html>`_
for more info!


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

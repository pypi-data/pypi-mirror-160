Readme for partis
=================


Utilities for defining and validating schemas for YAML/JSON compatible data, and
for configuring and running programs/workflows using the domain specific
Nano Workflow Language (NWL).


Installation
------------

Compatible with Python >= 3.6, pip >= 18.1.

For full install of core API, docs, runtime utilities, and GUI application:

.. code-block:: bash

  python3 make_dists.py
  pip3 install --find-links ./dist partis

To install only a particular set of sub-component(s), such as the nwl command-line runner:

.. code-block:: bash

  pip3 install --find-links ./dist partis-pyproj
  pip3 install --find-links ./dist partis-utils
  pip3 install --find-links ./dist partis-schema
  pip3 install --find-links ./dist partis-nwl

Note that unless distributions have already been generated and made available to
pip, these must be done in the above order.

Building the Documentation
--------------------------

The ``doc`` folder is made as a runnable python module to conveniently
build documentation.
By default, html documentation will be generated in a ``build`` directory.

.. code-block:: bash

  pip3 install --find-links ./dist '.[doc]'
  python -m doc

.. note::

  Any changes to source-code will not be reflected until the package is rebuilt.

Running the Tests
-----------------

The ``test`` folder is made as a runnable python module to conveniently
run automated test suite.

To test the GUI, Xvfb must also be installed on the system to create
a virtual display in order to run the Qt application without displaying windows.
If Xvfb is not found those tests will be skipped.

To test multiple versions of python, they must all be discoverable within the
``PATH`` environment variable.
The tests configured for versions of python that cannot be found will be skipped.
For example, if the python installations are being managed with the Environment
Modules convention:

.. code:: bash

  module load python/3.6.2
  module load python/3.7.0
  module load python/3.8.0
  module load python/3.9.0

It is highly recommended to install package and dependencies within a virtual
environment to isolate the effects of any changes it may cause.

.. code:: bash

  pip install --find-links ./dist '.[test]'
  python -m test

Development
===========

pre-commit
----------

Before committing any changes to this repo, please install pre-commit and hooks.

.. code-block:: bash

  pip install pre-commit
  pre-commit install
  pre-commit run --all-files

A convenience script ``runme.py`` is placed in the root directory to perform this action,
and needs to be run only once.

.. note::

  The ``pre-commit`` program is installed as a Python package.
  If a virtual environment is used during development, ensure that ``pre-commit``
  is installed in the environment active at the time of any commit.

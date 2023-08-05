.. -*- coding: utf-8 -*-

=======================================
 Rudderlabs Data Apps Utility Functions
=======================================

    This package containes scripts for creating new data apps project and running data apps pipeline using amazon sagemaker instance.


Development
-----------

Conda environment setup
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

    # Create the enviroment
    $ conda env create -f conda/environment.yaml
    # Activate and install this repository in edit mode
    $ conda activate rudderlabs
    $ pip install -e .


Code checks
~~~~~~~~~~~

    All the staged code changes needs to be passed pre-commit checks before committed and pushed to the remote repository

.. code-block:: bash

    #Adding all changes to staging
    $ git add --all

    #Running pre-commmit checks
    $ pre-commit run


Documentation
-------------

    All the documentation written in `ReStructuredText`_ markup language, located in `docs`_ folder. HTML files for documentation can be generated using `Sphinx`_ document generator.

.. code-block:: sh

    #html documentation building
    $ sphinx-build docs docs/html


.. Place your references here:
.. _ReStructuredText: https://docutils.sourceforge.io/rst.html
.. _Sphinx: https://www.sphinx-doc.org/en/master
.. _docs: ./docs

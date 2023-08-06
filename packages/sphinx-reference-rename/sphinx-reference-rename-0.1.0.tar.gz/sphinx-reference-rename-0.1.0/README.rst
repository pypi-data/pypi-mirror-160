sphinx-reference-rename
=======================

This Sphinx extension allows you to rename a code reference prior to Intersphinx
looking up the name. It exists to fix up some oddities that occur when you
combine type hints (`sphinx-autodoc-typehints`__) with Intersphinx references.
For some objects defined in C extension modules, the fully-qualified name of the
object is not the same as the one which is documented in the project's
``objects.inv`` file.

__ https://github.com/tox-dev/sphinx-autodoc-typehints

For example, Pandas and Requests have some objects which are documented under a
different name than their fully-qualified module name:

- ``pandas.DataFrame`` is documented under that name, but when imported, it
  reports that its fully-qualified name is ``pandas.core.frame.DataFrame``
- ``requests.Request`` reports that it is ``requests.models.Request``

.. code:: python

    >>> import pandas
    >>> pandas.DataFrame
    <class 'pandas.core.frame.DataFrame'>
    >>> import requests
    >>> requests.Request
    <class 'requests.models.Request'>

Since sphinx-autodoc-typehints has to rely on this fully-qualified name, and the
fully-qualified name doesn't match the one in these projects' documentation, the
link won't resolve. You can read more about the issue `here`__.

__ https://github.com/tox-dev/sphinx-autodoc-typehints/issues/47

Solving the Problem
-------------------

To resolve this, install this module via pip:

.. code:: bash

    pip install sphinx-reference-rename

Add the extension in your conf.py, and put it before `sphinx.ext.intersphinx`:

.. code:: python

    extensions = [
        # ...
        "sphinx_reference_rename",
        "sphinx.ext.intersphinx",
        # ...
    ]

Finally, create a dictionary named ``sphinx_reference_rename_mapping`` which
maps fully-qualified names to the fixed names. For example, given the examples
above:

.. code:: python

    sphinx_reference_rename_mapping = {
        "pandas.core.frame.DataFrame": "pandas.DataFrame",
        "requests.models.Request": "requests.Request",
    }

Now, your sphinx build should succeed!

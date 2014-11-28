## FOIA Docs

To read the docs, visit [FOIA Hub on Read the Docs](http://foia-hub.readthedocs.org/).

To build the docs locally, follow the instructions below.

This folder contains docs that are built using [Sphinx](http://sphinx-doc.org/index.html).

Sphinx is installed if you install the [dev-requirements.txt](https://github.com/18F/foia-hub/blob/master/requirements-dev.txt) or you can install it individually using the following command.

```
pip install sphinx
```

To build the docsusing Sphinx, from inside the docs folder, run the following.
```
make html
```

The Makefile will build the docs in the build directory. Once it is completely, you can preview the docs by visiting `build/html/index.html` in your browser.

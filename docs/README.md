## FOIA Docs

To read the docs, visit [FOIA Hub on Read the Docs](http://foia-hub.readthedocs.org/).

To build the docs locally, follow the instructions below.

This folder contains docs that are built using [Sphinx](http://sphinx-doc.org/index.html).

 To view the docs, run the following commands:
```
pip install sphinx
```

From inside the docs folder:
```
make html
```

The Makefile will build the docs in the build directory. Once it is completely, you can preview the docs by visiting `build/html/index.html` in your browser.

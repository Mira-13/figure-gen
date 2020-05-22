Overview
=========
This is an awesome figure generator. It generates figures.

Dependencies
================
- python 3.5+ (and in path)
- latex (either on win or linux)
- poppler (and in path).

The following python packages need to be installed:
```
python -m pip install --user matplotlib python-pptx pyexr pdf2image scipy imageio
```
Note that matplotlib version >3.2.1 is required for the constrained layout feature.
In case of install issues on Windows, try the pre-built OpenEXR binaries: https://www.lfd.uci.edu/~gohlke/pythonlibs/#openexr 

Getting started
================
Build and install the package:
```
python setup.py sdist bdist_wheel 
python -m pip install --user --upgrade --force-reinstall .\dist\figuregen-0.1-py3-none-any.whl
```
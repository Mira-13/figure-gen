# Figure Generator

This is an awesome figure generator. It generates figures.

## Quickstart

### Linux / Mac OS

```
./setup.sh
```

### Windows

Install the pre-built OpenEXR binaries: https://www.lfd.uci.edu/~gohlke/pythonlibs/#openexr
```
./setup.ps1
```

## Dependencies

- Python 3.5+ (and in path)
- LaTeX

The following python packages need to be installed:
```
python -m pip install --user matplotlib python-pptx pyexr scipy opencv-python wheel
```
Note that matplotlib version >3.2.1 is required for the constrained layout feature.
In case of install issues on Windows, try the pre-built OpenEXR binaries:
https://www.lfd.uci.edu/~gohlke/pythonlibs/#openexr

## Testing

There are two ways to run the unit tests: using Visual Studio or using Python CLI.

For Visual Studio, simply open the FigureGenerator.sln file and launch the debugger.

For Python CLI, the process is a bit more complicated. First, set PYTHONPATH to include the root folder of this repository.
Alternatively, you can install the package via pip, as discussed below. Then, you can run test as follows:
```
cd tests
python -m single_module
python -m multi_module
...
```

## Getting started

Build and install the package:
```
python setup.py sdist bdist_wheel
python -m pip install --user --upgrade --force-reinstall ./dist/figuregen-0.1-py3-none-any.whl
```
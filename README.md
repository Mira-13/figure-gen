# Figure Generator

This is an awesome figure generator. It generates figures in pdf-, html- and pptx-format.
The following image shows the output of one of our test files ("tests/pool.py"):
![](multi-module.png)

This tool might help not only to create final figures, but also to analyze images faster: We offer a bunch of error metrics that allows not only to compare images visually but also mathematically.

Why did we implemented a figure generator?

In rendering research, it is quite common to create figures of "comparison"-type. Meaning, that we start with a set of generated images, that needs to be compared. Oftentimes, one rendered scene is not enough, therefore, we need several comparison figures - at best in a similar or same style as the other created figures.

We support _grids_ (images that are grid-like arranged) and simple _line-plotting_. To get a further understanding what _grids_ are, you might want to have a look at our tutorial (Tutorial.ipynb).

## Quickstart

### Linux / Mac OS

```
./setup.sh
```

### Windows

Install the pre-built OpenEXR binaries: https://www.lfd.uci.edu/~gohlke/pythonlibs/#openexr

Dummy Note -to be more precise-: Open Powershell in folder where the downloaded binary file is:
``` 
python -m pip install .\OpenEXR-_VERSION_.whl
```

Afterwards, go to the main folder of the figure generator and run:
```
./setup.ps1
```
Dummy Note -in case this fails-: You might need to change execution policy to run the setup. Therefore, run in admin-Powershell:
```
Set-ExecutionPolicy Unrestricted
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

To get an inspiration on how to create figures, you might have a look at our tests or our [tutorial](Tutorial.ipynb).

## Feedback

We are happy to recieve honest feedback. If something does not work or you think there is a missing feature, please let us now.

WIP: We are planning to add a short questionnaire in the future.


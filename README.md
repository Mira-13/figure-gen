# Figure Generator

This is an awesome figure generator. It generates figures in pdf-, html- and pptx-format.
The following image shows the output of one of our test files ("tests/pool.py"):
![](multi-module.png)

This tool might help not only to create final figures, but also to analyze images faster: We offer a bunch of error metrics that allows not only to compare images visually but also mathematically.

Why did we create a figure generator?

In rendering research, it is quite common to create figures of "comparison"-type. Meaning, that we start with a set of generated images, that needs to be compared. Often, one rendered scene is not enough, therefore, we need several comparison figures - preferably in a similar or same style as the other created figures.

We support _grids_ (images that are grid-like arranged) and simple _line-plotting_. To get a further understanding what _grids_ are, you might want to have a look at our tutorial ([Tutorial.ipynb](Tutorial.ipynb)).

## Dependencies

- Python 3.6+
- LaTeX with the following packages: tikz, standalone, graphicx, fontenc, libertine, inputenc, comment, amsmath, newverbs.

(Optional) To include pdf files as image data, we offer a class figuregen.PDF. This class needs additional dependencies: PyPDF2, and pdf2image ([which requires poppler](https://pypi.org/project/pdf2image/)).

## Quickstart

To get an inspiration on how to create figures, you might have a look at our tests or our [tutorial](Tutorial.ipynb).

### Linux / Mac OS

```
python -m pip install figuregen
```

### Windows

Download the pre-built OpenEXR binaries: https://www.lfd.uci.edu/~gohlke/pythonlibs/#openexr
Open Powershell in the folder where the downloaded binary file is and run:
``` 
python -m pip install .\OpenEXR-_VERSION_.whl
python -m pip install figuregen
```

## Feedback 

We are happy to recieve honest feedback. If something does not work or you think there is a missing feature, please let us know.

Please participate in our survey (2-3 min):
https://forms.office.com/Pages/ResponsePage.aspx?id=DQSIkWdsW0yxEjajBLZtrQAAAAAAAAAAAAMAAAHGrp1UMDBNU0VaNVlXNjhDT1JVT1NXOUtNQlVYSy4u.

## Examples

Clicking on an image below leads to the test that created the corresponding figure.

### Vertical stacks
[<img src="tests/vertical-stack.png" width="600"/>](tests/vertical_stack.py)
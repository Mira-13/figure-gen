#PDF imports
from pdf2image import convert_from_path
import IPython
from IPython.display import Image
from IPython.display import display
import simpleimageio
import numpy as np

# HTML imports
from IPython.core.display import HTML
import re

def loadpdf(pdfname, dpi=1000):
    images = convert_from_path(pdfname, dpi=dpi)
    return np.array(images[0])

def convert(pdfname, dpi=1000):
    img = loadpdf(pdfname, dpi)
    simpleimageio.write(pdfname.replace('.pdf', '.png'), simpleimageio.srgb_to_lin(img / 255))
    return pdfname.replace('.pdf', '.png')

def displaypdf(pdfname):
    filename = convert(pdfname)
    IPython.display.display(Image(filename))

def loadhtml(html_file):
    with open(html_file) as f:
        html = f.read()
        figure = (re.findall(r"<body>(.*)</body>", html, re.DOTALL)[0])

        table = {
            "module": "position: absolute; ",
            "title-container": "position: absolute; margin-top: 0; margin-bottom: 0;display: flex; align-items: center; justify-content: center; ",
            "title-content": "margin-top: 0; margin-bottom: 0;",
            "element": "position: absolute; margin: 0; "
        }

        for c, s in table.items():
            figure = figure.replace(f'class="{c}" style="', f'class="{c}" style="{s}')
            figure = figure.replace(f'class="{c}"', '')

        return figure

def displayhtml(html_file):
    display(HTML(data=loadhtml(html_file)))